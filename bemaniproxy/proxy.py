from flask import Flask, g, request, Response
import requests
import json
import traceback

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
        to_server = request.data

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
        data=to_server
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
        to_game = server_response.content

    return respond_encoded(
        to_game,
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
        try:
            resp = handle(data, CONFIG)
        except:
            traceback.print_exc()
            return None
        if resp is None:
            return None
        if resp.name == data.name:
            return resp
        root = Node.void(data.name)
        resp.set_attribute("status", "0")
        root.add_child(resp)
        return root
    print("No method")
    return None


def handle_game(decoded: Node) -> Node:
    print("> {}".format(decoded.children[0].name))
    return handle_data(decoded, {
        "eacoin": create_eacoin_request,
        "pcbevent": create_pcbevent_request,
        "cardmng": create_cardmng_request,
        "game": create_game_request,
        "game_2": create_game_request,  # SDVX2
        "game_3": create_game_request   # SDVX3, museca
    })


def handle_server(decoded: Node) -> Node:
    print("< {}".format(decoded.children[0].name))
    return handle_data(decoded, {
        "services": create_services_response,
        "facility": create_facility_response,
        "eacoin": create_eacoin_response,
        "game": create_game_response
    })


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()
