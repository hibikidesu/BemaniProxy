from bemaniproxy.ea.node import Node
from bemaniproxy.ea import MODULES


def item(name: str, url: str) -> Node:
    node = Node.void('item')
    node.set_attribute('name', name)
    node.set_attribute('url', url)
    return node


def create_services(data: Node, extra: dict) -> Node:
    print(data)
    root = Node.void("services")
    root.set_attribute("expire", "600")
    root.set_attribute("mode", "operation")
    root.set_attribute("product_domain", "1")

    for name in MODULES:
        root.add_child(item(name, "http://{}:{}/".format(extra.get("host"), extra.get("port"))))

    root.add_child(item("ntp", "ntp://pool.ntp.org/"))
    root.add_child(item(
        "keepalive",
        "ping://{0}/?pa={0}&amp;ia={0}&amp;ga={0}&amp;ma={0}&amp;t1=2&amp;t2=10".format(extra.get("host"))
    ))
    print(root)

    return root
