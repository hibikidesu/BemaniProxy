from .proxy import *
import sys


def run():
    proxy = Proxy(host=get_host_address(), port=8050, game_server=sys.argv[1])
    proxy.run()
