from bemaniproxy.ea.node import Node


def create_pcbtracker_response(data: Node, config: dict):
    """Force disable """
    if config.get("options", {}).get("paseli") is False:
        data.child("pcbtracker").set_attribute("ecenable", "0")
        return data
    return None
