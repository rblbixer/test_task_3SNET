import sqlite3
import os
from typing import Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "test.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS runs (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT    NOT NULL,
                test_name TEXT    NOT NULL,
                status    TEXT    NOT NULL,
                duration  REAL    NOT NULL,
                output    TEXT    NOT NULL
            )
        """)


def save_run(
    timestamp: str,
    test_name: str,
    status: str,
    duration: float,
    output: str,
    run_id: Optional[int] = None,
) -> int:
    with get_connection() as conn:
        if run_id is None:
            cursor = conn.execute(
                "INSERT INTO runs (timestamp, test_name, status, duration, output) VALUES (?, ?, ?, ?, ?)",
                (timestamp, test_name, status, duration, output),
            )
            return cursor.lastrowid
        else:
            conn.execute(
                "UPDATE runs SET status = ?, duration = ?, output = ? WHERE id = ?",
                (status, duration, output, run_id),
            )
            return run_id


def get_run(run_id: int):
    with get_connection() as conn:
        return conn.execute("SELECT * FROM runs WHERE id = ?", (run_id,)).fetchone()


def get_all_runs():
    with get_connection() as conn:
        return conn.execute("SELECT * FROM runs ORDER BY id DESC").fetchall()
