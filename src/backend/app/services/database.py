import sqlite3
import os
from functools import lru_cache

@lru_cache
def get_db():
    conn = sqlite3.connect(os.environ.get("DB_PATH", "scholarship.db"))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
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
    """)
    conn.execute("""
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
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS student_scholarships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            scholarship_id INTEGER NOT NULL,
            status TEXT DEFAULT 'interested',
            matched_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    return conn
