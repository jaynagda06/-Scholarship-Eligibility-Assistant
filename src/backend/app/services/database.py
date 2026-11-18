import os
import sqlite3


def _database_path():
    """Return the SQLite path.

    Vercel's filesystem is read-only apart from /tmp, so fall back to a
    temporary database there when running inside a Vercel Function. The
    database is recreated and seeded on cold start by the app lifespan.
    """
    default_path = "/tmp/scholarship.db" if os.environ.get("VERCEL") else "scholarship.db"
    return os.environ.get("DB_PATH", default_path)


def get_db():
    # A fresh connection per call avoids sharing a sqlite connection across
    # the threads FastAPI uses for sync endpoints.
    conn = sqlite3.connect(_database_path(), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS scholarships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            org TEXT NOT NULL,
            category TEXT NOT NULL,
            eligibility_criteria TEXT NOT NULL,
            deadline TEXT NOT NULL,
            documents TEXT NOT NULL,
            url TEXT,
            status TEXT DEFAULT 'active'
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            school TEXT,
            degree TEXT,
            year INTEGER,
            annual_income REAL,
            category TEXT,
            disability_pct INTEGER,
            preferred_language TEXT DEFAULT 'en',
            created_at TEXT DEFAULT (datetime('now'))
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS student_scholarships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            scholarship_id INTEGER NOT NULL,
            status TEXT DEFAULT 'interested',
            matched_at TEXT DEFAULT (datetime('now'))
        )
        """
    )
    conn.commit()
    return conn
