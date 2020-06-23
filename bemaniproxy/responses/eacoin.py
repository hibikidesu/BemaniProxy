from flask import g

from bemaniproxy.ea.node import Node


def eacoin_getlog():  # TODO
    root = Node.void("eacoin")
    return root


def create_eacoin_response(data: Node, config: dict):
    incoming_method = g.incoming.children[0].attribute("method")
    if incoming_method == "opcheckin":   # Operator check-in
        root = Node.void("eacoin")
        root.add_child(Node.string("sessid", "666"))
        return root
    elif incoming_method == "getlog":
        return eacoin_getlog()
    return None
