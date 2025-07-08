# db.py

import sqlite3
from datetime import date

DB_PATH = "feelwrite.db"

# --- Create Tables ---
def create_tables():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Users table (if not already in auth.py)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        # Diary Entries table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                entry_date TEXT,
                content TEXT,
                mood TEXT,
                tags TEXT,
                image_path TEXT,
                last_updated TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        conn.commit()

# --- Add Entry ---
def add_entry(user_id, entry_date, content, mood, tags, image_path):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            INSERT INTO entries (user_id, entry_date, content, mood, tags, image_path, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, DATE('now'))
        ''', (user_id, entry_date, content, mood, tags, image_path))
        conn.commit()

# --- Update Existing Entry ---
def update_entry(user_id, entry_date, content, mood, tags, image_path):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            UPDATE entries
            SET content = ?, mood = ?, tags = ?, image_path = ?, last_updated = DATE('now')
            WHERE user_id = ? AND entry_date = ?
        ''', (content, mood, tags, image_path, user_id, entry_date))
        conn.commit()

# --- Get Entry By Date ---
def get_entry_by_date(user_id, entry_date):
    with sqlite3.connect(DB_PATH) as conn:
        result = conn.execute('''
            SELECT content, mood, tags, image_path
            FROM entries
            WHERE user_id = ? AND entry_date = ?
        ''', (user_id, entry_date)).fetchone()
    return result

# --- Get All Entries ---
def get_all_entries(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        result = conn.execute('''
            SELECT entry_date, mood, tags
            FROM entries
            WHERE user_id = ?
            ORDER BY entry_date DESC
        ''', (user_id,)).fetchall()
    return result
