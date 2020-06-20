from bemaniproxy.ea.node import Node
from bemaniproxy.database import get_db


def create_pcbevent_request(data: Node, config: dict):

    db = get_db()
    for item in data.children[0].children:
        if item.name == "item":
            db.insert_event(
                event=item.child_value("name"),
                t=item.child_value("time"),
                data=item.child_value("value")
            )

    return data
