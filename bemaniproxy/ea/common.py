import os
from binascii import hexlify
from string import digits, ascii_uppercase

from .node import Node

__all__ = [
    "generate_header",
    "generate_card",
    "generate_message_maint",
    "convert_game_to_user_id",
    "convert_user_id_to_game"
]
MAX_U_SIZE = (36**8) - 1
BASE_36 = digits + ascii_uppercase
ECS_STR = "{0:0>4}-{1:0>4}"


def generate_header():
    return "1-{}-{}".format(hexlify(os.urandom(4)).decode(), hexlify(os.urandom(2)).decode())


def generate_card():
    return "E004{}".format(hexlify(os.urandom(6)).decode().upper())


def generate_message_maint():
    n = Node.void("response")
    m = Node.void("message")

    def i(name: str):
        x = Node.void("item")
        x.set_attribute("end", "86400")
        x.set_attribute("name", name)
        x.set_attribute("start", "0")
        return x

    m.add_child(i("sys.mainte"))
    m.add_child(i("sys.eacoin.mainte"))

    m.set_attribute("expire", "300")
    m.set_attribute("status", "0")
    n.add_child(m)
    return n


def convert_game_to_user_id(game_id: str):
    """
    Converts game id to user id
    """
    # eight char string should be 9 chars in length
    if len(game_id) != 9:
        return -1

    # 5 place should be dash
    if game_id[4] != "-":
        return -1

    b36_str = game_id[:4] + game_id[5:]

    try:
        return int(b36_str, 36)
    except:
        return -1


def convert_user_id_to_game(user_id: int):
    """
    Converts user id to game id
    """
    if not 0 <= user_id <= MAX_U_SIZE:
        return ""

    b36_str = b10_to_b36(user_id)
    return ECS_STR.format(b36_str[:-4], b36_str[-4:])


def b10_to_b36(x):
    """
    Converts number from base 10 to base 36.
    NOTE: positive only.

    IN:
        x - number to convert

    RETURNS: base 36 number, or None if out of range
    """
    if x == 0:
        return BASE_36[0]

    digits = []
    while x > 0:
        digits.append(BASE_36[int(x % 36)])
        x = int(x / 36)

    digits.reverse()
    return "".join(digits)
