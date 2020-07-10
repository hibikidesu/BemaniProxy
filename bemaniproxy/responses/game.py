from flask import g

from bemaniproxy.ea.node import Node
from bemaniproxy.ea.game_ver import *
from bemaniproxy.database import get_db


def create_game_response(data: Node, config: dict):
    method = g.incoming.children[0].attribute("method")

    # if method == "sv5_load":
    #     game = data.child("game")

    # Unable to do this since megu long response times and game times out adding new scores
    # if method == "sv5_load_m":
    #     game = data.child("game")
    #     refid = g.incoming.children[0].child_value("refid")
    #     music = game.child("music").children
    #     db = get_db()
    #
    #     old_score_ids = []
    #
    #     # Update songs and find old scores if not exist
    #     for song in music:
    #         param = song.child_value("param")
    #         old_score_ids.append(param[0])
    #         db.save_game(
    #             SDVX.VIVID_WAVE, refid,
    #             song_id=param[0],
    #             music_type=param[1],
    #             score=param[2],
    #             clear_type=param[3],
    #             grade=param[4],
    #             btn_rate=param[7],
    #             long_rate=param[8],
    #             vol_rate=param[9]
    #         )
    #
    #     # Add songs which are not on network
    #     for score in db.get_scores(SDVX.VIVID_WAVE, refid):
    #         if score[3] not in old_score_ids:
    #             print(score)
    #             info = Node.void("info")
    #             param = Node.u32_array("param", [
    #                 score[3],
    #                 score[4],
    #                 score[6],
    #                 score[7],
    #                 score[8],
    #                 0,
    #                 0,
    #                 score[14],
    #                 score[15],
    #                 score[16],
    #                 0,
    #                 0,
    #                 0,
    #                 0,
    #                 0,
    #                 0
    #             ])
    #             info.add_child(param)
    #             game.child("music").add_child(info)
    #     return data

    return None
