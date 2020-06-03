from bemaniproxy.ea.node import Node


def create_eacoin_request(data: Node, config: dict):
    method = data.children[0].attribute("method")
    if method == "consume":     # Coin consume
        # If unlimited paseli is enabled swap out payment value for service coin
        if config.get("coin", {}).get("unlimited_paseli", False) is True:
            payment = data.child("eacoin/payment")
            service = data.child("eacoin/service")
            service.set_value(payment.value)
            payment.set_value(0)
    return data
