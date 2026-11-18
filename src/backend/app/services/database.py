import os
import sqlite3
import tempfile
import threading
import uuid

_path_lock = threading.Lock()


def _working_dir_is_writable():
    # A unique name per call: two processes probing at the same moment would
    # otherwise delete each other's file and both conclude "read-only".
    probe = os.path.join(os.getcwd(), ".db_write_probe_" + uuid.uuid4().hex)
    try:
        with open(probe, "w", encoding="utf-8") as handle:
            handle.write("")
        os.remove(probe)
        return True
    except OSError:
        return False


# Resolved once, under a lock. The probe creates and deletes a file, so running
# it per connection let concurrent requests race: one deleted the probe while
# another was still using it, the loser read "not writable" and fell back to a
# path that may not exist. That surfaced as intermittent 500s on first load.
_database_path_cache = None


def _database_path():
    """Return the SQLite path.

    Vercel's filesystem is read-only apart from /tmp, so fall back to a
    temporary database there. The database is recreated and seeded on cold
    start by the app lifespan.
    """
    global _database_path_cache
    if _database_path_cache is not None:
        return _database_path_cache

    with _path_lock:
        if _database_path_cache is not None:
            return _database_path_cache

        explicit = os.environ.get("DB_PATH")
        if explicit:
            resolved = explicit
        elif os.environ.get("VERCEL") or not _working_dir_is_writable():
            resolved = "/tmp/scholarship.db"
            if os.name == "nt":
                # "/tmp" is not a real path on Windows.
                resolved = os.path.join(tempfile.gettempdir(), "scholarship.db")
        else:
            resolved = "scholarship.db"

        _database_path_cache = resolved
        return resolved


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
