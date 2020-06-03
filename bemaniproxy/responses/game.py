from bemaniproxy.ea.node import Node
from bemaniproxy.database import get_db


def create_game_response(data: Node, config: dict):
    method = g.incoming.children[0].attribute("method")

    if method == "sv5_load":
        game = data.child("game")

    return data
