import sqlite3
from flask import g
from time import time

__all__ = ["Database", "get_db"]


class Database:

    def __init__(self):
        self.db = sqlite3.connect("bemaniproxy.db")
        self.setup()

    def save_game(self, game_version, card_id: str, *,
                  song_id: int, mode: int, score: int, clear_type: int, grade: int, max_chain: int,
                  critical: int, near: int, error: int, effective_rate: int, btn_rate: int, long_rate: int,
                  vol_rate: int, music_type: int):
        """Save a played game"""
        c = self.db.cursor()
        c.execute("SELECT score FROM scores WHERE card_id = ? AND song_id = ? AND music_type = ?",
                  (card_id, song_id, music_type))
        old_score = c.fetchone()
        if not old_score:
            # If not a prev score
            c.execute(
                "INSERT INTO scores VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                (
                    card_id,
                    int(time()),
                    game_version.name,
                    song_id,
                    music_type,
                    mode,
                    score,
                    clear_type,
                    grade,
                    max_chain,
                    critical,
                    near,
                    error,
                    effective_rate,
                    btn_rate,
                    long_rate,
                    vol_rate
                )
            )
        elif int(old_score[0]) < score:
            # Update prev score
            print("UPDATE PREV SCORE")
            c.execute(
                "UPDATE scores SET "
                "time = ?, "
                "mode = ?, "
                "score = ?, "
                "clear_type = ?, "
                "grade = ?, "
                "max_chain = ?, "
                "critical = ?, "
                "near = ?, "
                "error = ?, "
                "effective_rate = ?, "
                "btn_rate = ?, "
                "long_rate = ?, "
                "vol_rate = ? WHERE card_id = ? AND song_id = ? AND music_type = ?",
                (
                    int(time()),
                    mode,
                    score,
                    clear_type,
                    grade,
                    max_chain,
                    critical,
                    near,
                    error,effective_rate,
                    btn_rate,
                    long_rate,
                    vol_rate,
                    card_id,
                    song_id,
                    music_type
                )
            )
        self.db.commit()
        c.close()

    def insert_event(self, event: str, *, user: str = None, data: str = None):
        c = self.db.cursor()
        c.execute("INSERT INTO events VALUES (?, ?, ?, ?)", (event, int(time()), user, data))
        self.db.commit()
        c.close()

    def setup(self):
        """Setup the database"""
        c = self.db.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS scores ("
                  "card_id TEXT NOT NULL, "
                  "time INTEGER NOT NULL, "
                  "game TEXT NOT NULL, "
                  "song_id INTEGER NOT NULL, "
                  "music_type INTEGER NOT NULL, "
                  "mode INTEGER, "
                  "score INTEGER NOT NULL, "
                  "clear_type INTEGER, "
                  "grade INTEGER, "
                  "max_chain INTEGER NOT NULL, "
                  "critical INTEGER NOT NULL, "
                  "near INTEGER NOT NULL, "
                  "error INTEGER NOT NULL, "
                  "effective_rate INTEGER, "
                  "btn_rate INTEGER, "
                  "long_rate INTEGER, "
                  "vol_rate INTEGER)")
        c.execute("CREATE TABLE IF NOT EXISTS events ("
                  "event TEXT NOT NULL, "
                  "time INTEGER NOT NULL, "
                  "user TEXT, "
                  "data TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS users_sdvx ("
                  ")")
        self.db.commit()
        c.close()

    def close(self):
        self.db.close()


def get_db() -> Database:
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = Database()
    return db
