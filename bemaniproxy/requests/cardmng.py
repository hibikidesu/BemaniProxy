from bemaniproxy.ea.node import Node


def create_cardmng_request(data: Node, config: dict):
    method = data.children[0].attribute("method")
    options = config.get("card", {})



    return None
