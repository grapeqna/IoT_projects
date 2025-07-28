import sqlite3

DB_NAME = 'database.db'

conn = sqlite3.connect(DB_NAME)
conn.execute("PRAGMA foreign_keys=\"ON\"")

conn.cursor().execute('''
    CREATE TABLE IF NOT EXISTS devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        manufacturer TEXT NOT NULL,
        building TEXT NOT NULL
    )
''')

conn.cursor().execute('''
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id INTEGER NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        name TEXT NOT NULL,
        FOREIGN KEY(device_id) REFERENCES devices(id) ON DELETE CASCADE
    )
''')

conn.commit()