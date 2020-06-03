from bemaniproxy.proxy import *


def run():
    """Main entry, runs flask debug server"""
    app.run("0.0.0.0", 8050)
