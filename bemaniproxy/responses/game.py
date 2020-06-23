from flask import g

from bemaniproxy.ea.node import Node
from bemaniproxy.ea.game_ver import *
from bemaniproxy.database import get_db


def create_game_response(data: Node, config: dict):
    method = g.incoming.children[0].attribute("method")

    if method == "sv5_load":
        game = data.child("game")
    elif method == "sv5_load_m":
        game = data.child("game")
        refid = g.incoming.children[0].child_value("refid")
        db = get_db()
        for song in game.child("music").children:
            param = song.child_value("param")
            db.save_game(
                SDVX.VIVID_WAVE, refid,
                song_id=param[0],
                music_type=param[1],
                score=param[2],
                clear_type=param[3],
                grade=param[4],
                btn_rate=param[7],
                long_rate=param[8],
                vol_rate=param[9]
            )

    return None
