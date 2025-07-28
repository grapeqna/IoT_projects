import sqlite3

DB_NAME = 'database.db'

# Connect
conn = sqlite3.connect(DB_NAME)

conn.execute("PRAGMA foreign_keys=\"ON\"")

# Create motion sensors table
conn.cursor().execute('''
    CREATE TABLE IF NOT EXISTS motion_sensor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        manufacturer TEXT NOT NULL,
        room TEXT NOT NULL
    )
''')

# Create entries table
conn.cursor().execute('''
    CREATE TABLE IF NOT EXISTS motion_detection (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        motion_sensor_id INTEGER NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(motion_sensor_id) REFERENCES motion_sensor(id) ON DELETE CASCADE
    )
''')

# Commit changes
conn.commit()