from flask import Flask, g, request, Response
import requests
import json

from bemaniproxy.database import Database
from bemaniproxy.responses import *
from bemaniproxy.requests import *
from bemaniproxy.ea.protocol import EAmuseProtocol
from bemaniproxy.ea.node import Node

__all__ = ["app"]

app = Flask(__name__)
with open("config.json", "r") as f:
    CONFIG = json.load(f)


#
# Routes
#

@app.route("/", defaults={"path": ""}, methods=["POST"])
@app.route("/<path:path>", methods=["POST"])
def on_post(path: str):
    """
    Handle all posts, assuming is from the game, call the real server, handle the data and send it back to the game.
    :param path: url path
    :return: response
    """
    compression = request.headers.get("X-Compress", None)
    encryption = request.headers.get("X-Eamuse-Info", None)
    protocol = EAmuseProtocol()

    actual_path = "/{}".format(path)
    if request.query_string is not None and len(request.query_string) > 0:
        actual_path = actual_path + "?{}".format(request.query_string.decode("ascii"))

    print("Handling")

    # Decode the data
    decoded = protocol.decode(
        compression=compression,
        encryption=encryption,
        data=request.data
    )
    g.incoming: Node = decoded  # Some response methods may need to use this since the server may not send what we need
    modified_game = handle_game(decoded)
    if modified_game is not None:
        to_server = protocol.encode(
            compression=compression,
            encryption=encryption,
            tree=modified_game
        )
    else:
        to_server = None

    # Send to game server and receive data
    headers = {
        "Accept-Encoding": "identity, deflate, compress, gzip"
    }
    if compression is not None:
        headers["X-Compress"] = compression
    if encryption is not None:
        headers["X-Eamuse-Info"] = encryption
    if request.headers.get("User-Agent", None) is not None:
        headers["User-Agent"] = request.headers.get("User-Agent", None)

    prep_req = requests.Request(
        method="POST",
        url=CONFIG.get("server") + actual_path,
        headers=headers,
        data=to_server if to_server is not None else request.data
    ).prepare()
    sess = requests.Session()
    server_response = sess.send(prep_req, timeout=60)

    resp_protocol = EAmuseProtocol()

    resp_compression = server_response.headers.get("X-Compress", None)
    resp_encryption = server_response.headers.get("X-Eamuse-Info", None)
    try:
        server_decoded = resp_protocol.decode(
            compression=resp_compression,
            encryption=resp_encryption,
            data=server_response.content
        )
    except:
        print("FAILED TO DECODE SERVER")
        return respond_encoded(
            server_response.content,
            compression=resp_compression,
            encryption=resp_encryption
        )
    modified_server = handle_server(server_decoded)
    if modified_server is not None:
        to_game = resp_protocol.encode(
            compression=resp_compression,
            encryption=resp_encryption,
            tree=modified_server
        )
    else:
        to_game = None

    return respond_encoded(
        to_game if to_game is not None else server_response.content,
        compression=resp_compression,
        encryption=resp_encryption
    )


#
# Helpers
#

def respond_encoded(data: bytes, compression: str = None, encryption: str = None):
    response = Response(data)
    if compression is not None:
        response.headers["X-Compress"] = compression
    if encryption is not None:
        response.headers["X-Eamuse-Info"] = encryption
    return response


def handle_data(data: Node, handles: dict):
    handle = handles.get(data.children[0].name)
    if handle:
        resp = handle(data, CONFIG)
        if data == resp:
            return None
        if resp.name == data.name:
            return resp
        root = Node.void(data.name)
        resp.set_attribute("status", "0")
        root.add_child(resp)
        return root
    return None


def handle_game(decoded: Node) -> Node:
    print("> {}".format(decoded.children[0].name))
    return handle_data(decoded, {
        "eacoin": create_eacoin_request,
        "game": create_game_request
    })


def handle_server(decoded: Node) -> Node:
    print("< {}".format(decoded.children[0].name))
    return handle_data(decoded, {
        "services": create_services_response,
        "facility": create_facility_response,
        "eacoin": create_eacoin_response,
        "game": create_game_response,
        "pcbevent": create_pcbevent_response
    })


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

# def get_host_address():
#     return socket.gethostbyname(socket.gethostname())


# class Proxy:
#
#     def __init__(self, host: str, port: int, game_server: str, database: Database):
#         self.host: str = host
#         self.port: int = port
#         self.game_server: str = game_server
#         self.buffer_size = 4096
#         self.sock = None
#         self.db = database
#         self.out_handles = {
#             "services": create_services
#         }
#         self.in_handles = {}
#
#     def __send_to_game_server(self, data: bytes) -> bytes:
#         server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         try:
#             # Connect to game server
#             server.connect((self.game_server, 80))
#         except Exception as e:
#             print("Failed to conntect to game server. {}".format(e))
#             return b""
#
#         # Send all our data from game
#         server.send(data)
#
#         # Receive data from server
#         server_data = b""
#         while True:
#             chunk = server.recv(self.buffer_size)
#             if not chunk:
#                 break
#             server_data += chunk
#
#         print("Server resp size : {}".format(len(server_data)))
#         server.close()
#         return server_data
#
#     def _handle_request(self, req: Node) -> Node:
#         data = req.children[0]
#         print("> {}".format(data.name))
#
#         request_handle = self.out_handles.get(data.name, None)
#         if request_handle is None:
#             print("No handle for {}".format(data.name))
#             return req
#
#         resp = request_handle(req, {
#             "host": self.host,
#             "port": self.port
#         })
#         root = Node.void("response")
#         resp.set_attribute("status", "0")
#         root.add_child(resp)
#
#         return root
#
#     @staticmethod
#     def _parse_http(data: bytes) -> tuple:
#         parser = HttpParser()
#         assert parser.execute(data, len(data)) == len(data)
#         return parser.recv_body(), parser.get_headers()
#
#     @staticmethod
#     def _decode_http(body: bytes, headers) -> Union[Tuple[EAmuseProtocol, Node], Tuple[None, None]]:
#         # Get the headers
#         key = headers.get("X-Eamuse-Info")
#         compression = headers.get("X-Compress")
#
#         # Decode data
#         protocol = EAmuseProtocol()
#         try:
#             decoded = protocol.decode(compression, key, body)
#             return protocol, decoded
#         except:
#             print("Failed to decode")
#             return None, None
#
#     def _parse_server_data(self, data: bytes) -> bytes:
#         """
#         Parse the server data, decrypt it, read it, encrypt it and send back to game
#         :param data: Server data response
#         :return: Modified data
#         """
#
#         body, headers = self._parse_http(data)
#         protocol, req = self._decode_http(body, headers)
#         if req is None:
#             return data
#
#         # Send response
#         root = self._handle_request(req)
#
#         key = headers.get("X-Eamuse-Info")
#         compression = headers.get("X-Compress")
#
#         # Create headers
#         response = "HTTP/1.1 200 OK\r\n"
#         if compression:
#             response += "X-Compress: {}\r\n".format(compression)
#         else:
#             response += "X-Compress: none\r\n"
#         if key:
#             response += "X-Eamuse-Info: {}\r\n".format(key)
#         response += "\r\n"
#         response = response.encode()
#
#         # Encode and send body
#         response += protocol.encode(compression, key, root)
#
#         return response
#
#     def _handle(self, client, addr):
#         print("Handling {}".format(addr[0]))
#         # Receive data
#         data = b""
#         while True:
#             chunk = client.recv(self.buffer_size)
#             data += chunk
#             if len(chunk) < self.buffer_size:
#                 break
#
#         # body, headers = self._parse_http(data)
#         # protocol, req = self._decode_http(body, headers)
#         # if req:
#         #     print("< {}".format(req.children[0].name))
#         #     hndl = self.in_handles.get(req.children[0].name)
#         #     if hndl:
#         #         hndl(req, {
#         #             "host": self.host,
#         #             "port": self.port
#         #         })
#
#         # Receive data from the game server
#         server_data = self.__send_to_game_server(data)
#
#         # Parse server body as it is the data which is going to be sent
#         send_data = self._parse_server_data(server_data)
#
#         # Send data to client
#         client.send(send_data)
#         client.close()
#
#     def __listen(self):
#         # Check if sock is not None
#         if self.sock is None:
#             raise Exception("Socket has not yet been created.")
#         # Accept max 5 connections at once
#         self.sock.listen(5)
#
#         # Accept connections and start handling them
#         while True:
#             try:
#                 client, addr = self.sock.accept()
#             except KeyboardInterrupt:
#                 self.close()
#                 return
#
#             client.settimeout(60)
#             threading.Thread(target=self._handle, args=(client, addr)).start()
#
#     def run(self):
#         # Bind socket to address
#         self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.sock.bind((self.host, self.port))
#         print("Proxy - http://{}:{}".format(self.host, self.port))
#
#         self.__listen()
#
#     def close(self):
#         try:
#             # Try to shutdown the socket
#             self.sock.shutdown(socket.SHUT_RDWR)
#             self.sock = None
#             print("Proxy has been shut down")
#         except:
#             pass

