import sqlite3
from flask import g
from time import time

__all__ = ["Database", "get_db"]


class Database:

    def __init__(self):
        self.db = sqlite3.connect("bemaniproxy.db")
        self.setup()

    def get_scores(self, game_version, refid: str) -> list:
        c = self.db.cursor()
        c.execute("SELECT * FROM scores WHERE refid = ? AND game = ?", (refid, game_version.name))
        data = c.fetchall()
        c.close()
        return data

    def save_game(self, game_version, refid: str, *,
                  song_id: int = 0, mode: int = 0, score: int = 0, clear_type: int = 0, grade: int = 0,
                  max_chain: int = 0, critical: int = 0, near: int = 0, error: int = 0, effective_rate: int = 0,
                  btn_rate: int = 0, long_rate: int = 0, vol_rate: int = 0, music_type: int = 0):
        """Save a played game"""
        c = self.db.cursor()
        c.execute("SELECT score FROM scores WHERE refid = ? AND song_id = ? AND music_type = ?",
                  (refid, song_id, music_type))
        old_score = c.fetchone()
        if not old_score:
            # If not a prev score
            c.execute(
                "INSERT INTO scores VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                (
                    refid,
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
                "vol_rate = ? WHERE refid = ? AND song_id = ? AND music_type = ?",
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
                    refid,
                    song_id,
                    music_type
                )
            )
        self.db.commit()
        c.close()

    def insert_event(self, event: str, *, t: int = None, user: str = None, data: str = None):
        c = self.db.cursor()
        c.execute("INSERT INTO events VALUES (?, ?, ?, ?)", (event, int(time()) if t is None else t, user, data))
        self.db.commit()
        c.close()

    def setup(self):
        """Setup the database"""
        c = self.db.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS scores ("
                  "refid TEXT NOT NULL, "
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
        self.db.commit()
        c.close()

    def close(self):
        self.db.close()


def get_db() -> Database:
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = Database()
    return db
