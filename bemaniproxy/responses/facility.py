from bemaniproxy.ea.node import Node


def create_facility_response(data: Node, config: dict) -> Node:
    share_url = data.child("facility/share/url")
    share_options = config.get("options", {}).get("server_name", {})
    if share_url is not None and share_options:
        # Swap out names to config names
        for name in ["eapass", "arcadefan", "konaminetdx", "konamiid", "eagate"]:
            if share_options.get(name):
                url_node = share_url.child(name)
                if url_node:
                    url_node.set_value(share_options.get(name))
    return data
