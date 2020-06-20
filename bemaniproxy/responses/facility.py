from bemaniproxy.ea.node import Node


def create_facility_response(data: Node, config: dict) -> Node:
    share_url = data.child("facility/share/url")
    options = config.get("options", {}).get("server_name", {})
    if not options:
        return data
    if share_url is not None:
        # Swap out names to config names
        for name in ["eapass", "arcadefan", "konaminetdx", "konamiid", "eagate"]:
            if options.get(name):
                url_node = share_url.child(name)
                if url_node:
                    url_node.set_value(options.get(name))
    location = data.child("facility/location")
    if location:
        for name in ["country", "name", "regionjname", "id"]:
            if options.get(name):
                location.child(name).set_value(options.get(name))

    return data
