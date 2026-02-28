import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "hiresight.db"


def create_connection():
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def _column_exists(conn, table_name, column_name):
    rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return any(row[1] == column_name for row in rows)


def _ensure_history_columns(conn):
    required_columns = {
        "filename": "TEXT",
        "missing_skills": "TEXT",
        "strengths": "TEXT",
        "recommendations": "TEXT",
        "created_at": "TEXT",
    }

    for column, column_type in required_columns.items():
        if not _column_exists(conn, "history", column):
            conn.execute(f"ALTER TABLE history ADD COLUMN {column} {column_type}")
            if column == "created_at":
                conn.execute(
                    "UPDATE history SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL"
                )


def _ensure_user_columns(conn):
    if not _column_exists(conn, "users", "created_at"):
        conn.execute("ALTER TABLE users ADD COLUMN created_at TEXT")
        conn.execute("UPDATE users SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL")


def create_tables():
    def _init_schema(conn):
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                filename TEXT,
                match_score REAL NOT NULL,
                grade TEXT NOT NULL,
                missing_skills TEXT,
                strengths TEXT,
                recommendations TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        _ensure_user_columns(conn)
        _ensure_history_columns(conn)
        conn.commit()

    conn = None
    try:
        conn = create_connection()
        _init_schema(conn)
    except sqlite3.DatabaseError as exc:
        if "malformed" not in str(exc).lower():
            raise

        if conn is not None:
            conn.close()
            conn = None

        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = DB_PATH.with_name(f"{DB_PATH.stem}.corrupt.{stamp}{DB_PATH.suffix}")
        if DB_PATH.exists():
            DB_PATH.replace(backup)

        conn = create_connection()
        _init_schema(conn)
    finally:
        if conn is not None:
            conn.close()
