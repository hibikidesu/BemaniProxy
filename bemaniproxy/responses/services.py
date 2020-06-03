from flask import request

from bemaniproxy.ea.node import Node
from bemaniproxy.ea import MODULES


def item(name: str, url: str) -> Node:
    node = Node.void("item")
    node.set_attribute("name", name)
    node.set_attribute("url", url)
    return node


def create_services_response(data: Node, config: dict) -> Node:
    """
    Replace the servers urls with our urls to direct all traffic from the game to us
    :param data: Response from server
    :param extra: Extra params
    :return: Services data
    """
    root = Node.void("services")
    root.set_attribute("expire", "600")
    root.set_attribute("mode", "operation")
    root.set_attribute("product_domain", "1")

    for name in MODULES:
        root.add_child(item(name, "http://{}:8050/".format(request.host)))

    root.add_child(item("ntp", "ntp://pool.ntp.org/"))
    root.add_child(item(
        "keepalive",
        "ping://{0}/?pa={0}&amp;ia={0}&amp;ga={0}&amp;ma={0}&amp;t1=2&amp;t2=10".format(request.host)
    ))

    return root
