import socket
import threading
import traceback
from .responses import *
from bemaniproxy.ea.protocol import EAmuseProtocol
from bemaniproxy.ea.node import Node
try:
    from http_parser.parser import HttpParser
except ImportError:
    from http_parser.pyparser import HttpParser

__all__ = ["get_host_address", "Proxy"]


def get_host_address():
    return socket.gethostbyname(socket.gethostname())


class Proxy:

    def __init__(self, host: str, port: int, game_server: str):
        self.host: str = host
        self.port: int = port
        self.game_server: str = game_server
        self.buffer_size = 512
        self.sock = None
        self.handles = {
            "services": create_services
        }

    def __send_to_game_server(self, data: bytes) -> bytes:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Connect to game server
            server.connect((self.game_server, 80))
        except Exception as e:
            print("Failed to conntect to game server. {}".format(e))
            return b""

        # Send all our data from game
        server.sendall(data)

        # Receive data from server
        server_data = b""
        while True:
            part = server.recv(self.buffer_size)
            server_data += part
            if len(part) < self.buffer_size:
                break

        server.close()
        return server_data

    def _handle_request(self, req: Node) -> Node:
        data = req.children[0]
        print("> {}".format(data.name))

        request_handle = self.handles.get(data.name, None)
        if request_handle is None:
            print("No handle for {}".format(data.name))
            return req

        resp = request_handle(req, {
            "host": self.host,
            "port": self.port
        })
        root = Node.void("response")
        resp.set_attribute("status", "0")
        root.add_child(resp)

        return root

    def _parse_server_data(self, data: bytes) -> bytes:
        """
        Parse the server data, decrypt it, read it, encrypt it and send back to game
        :param data: Server data response
        :return: Modified data
        """
        parser = HttpParser()
        assert parser.execute(data, len(data)) == len(data)

        body = parser.recv_body()
        if not body:
            return data

        headers = parser.get_headers()
        key = headers.get("X-Eamuse-Info")
        compression = headers.get("X-Compress")

        protocol = EAmuseProtocol()
        try:
            req = protocol.decode(compression, key, body)
        except:
            print("Failed to decode")
            return data
        if req is None:
            print("Failed to decode")
            return data

        # Send response
        root = self._handle_request(req)

        # Create headers
        response = "HTTP/1.1 200 OK\r\n"
        if compression:
            response += "X-Compress: {}\r\n".format(compression)
        else:
            response += "X-Compress: none\r\n"
        if key:
            response += "X-Eamuse-Info: {}\r\n".format(key)
        response += "\r\n"
        response = response.encode()

        # Encode and send body
        response += protocol.encode(compression, key, root)

        return response

    def _handle(self, client, addr):
        print("Handling {}".format(addr[0]))
        # Receive data
        data = b""
        while True:
            part = client.recv(self.buffer_size)
            data += part
            if len(part) < self.buffer_size:
                break

        # Receive data from the game server
        server_data = self.__send_to_game_server(data)

        # Parse server body as it is the data which is going to be sent
        send_data = self._parse_server_data(server_data)

        # Send data to client
        client.sendall(send_data)
        client.close()

    def __listen(self):
        # Check if sock is not None
        if self.sock is None:
            raise Exception("Socket has not yet been created.")
        # Accept max 5 connections at once
        self.sock.listen(5)

        # Accept connections and start handling them
        while True:
            try:
                client, addr = self.sock.accept()
            except KeyboardInterrupt:
                self.close()
                return

            client.settimeout(60)
            threading.Thread(target=self._handle, args=(client, addr)).start()

    def run(self):
        # Bind socket to address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        print("Proxy - http://{}:{}".format(self.host, self.port))

        self.__listen()

    def close(self):
        try:
            # Try to shutdown the socket
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock = None
            print("Proxy has been shut down")
        except:
            pass
