from bemaniproxy.ea.node import Node
from bemaniproxy.ea.model import Model
from bemaniproxy.ea import game_ver
from bemaniproxy.database import get_db


def save_sv_game(game: Node, version: str):
    db = get_db()
    db.save_game(
        game_version=game_ver.get_version_string(Model.from_modelstring(version)),
        refid=game.child_value("dataid"),
        song_id=game.child_value("music_id"),
        music_type=game.child_value("music_type"),
        mode=game.child_value("mode"),
        score=game.child_value("score"),
        clear_type=game.child_value("clear_type"),
        grade=game.child_value("score_grade"),
        max_chain=game.child_value("max_chain"),
        critical=game.child_value("critical"),
        near=game.child_value("near"),
        error=game.child_value("error"),
        effective_rate=game.child_value("effective_rate"),
        btn_rate=game.child_value("btn_rate"),
        long_rate=game.child_value("long_rate"),
        vol_rate=game.child_value("vol_rate")
    )


def create_game_request(data: Node, config: dict):
    """Handle game out logic such as score tracking"""
    method = data.children[0].attribute("method")

    if method == "sv5_save_m":      # SDVX 5 song save request
        save_sv_game(data.child("game"), data.attribute("model"))
    elif method == "sv4_save_m":    # SDVX 4
        save_sv_game(data.child("game"), data.attribute("model"))
    elif method == "save_m":        # <4
        save_sv_game(data.children[0], data.attribute("model"))

    return None
