import sqlite3
from contextlib import contextmanager

DB_PATH = "data/matches.db"

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team1 TEXT, team2 TEXT,
                team1_score TEXT, team2_score TEXT,
                venue TEXT, match_date TEXT,
                result TEXT, key_stats TEXT
            )
        """)
        conn.commit()

def insert_match(match_data: dict):
    with get_db() as conn:
        conn.execute("""
            INSERT INTO matches (team1, team2, team1_score, team2_score, venue, match_date, result, key_stats)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            match_data["team1"], match_data["team2"],
            match_data["team1_score"], match_data["team2_score"],
            match_data["venue"], match_data["match_date"],
            match_data["result"], match_data["key_stats"]
        ))
        conn.commit()

def get_match(match_id: int):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM matches WHERE id = ?", (match_id,)).fetchone()
        return dict(row) if row else None