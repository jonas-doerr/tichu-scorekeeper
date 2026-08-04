import sqlite3

conn = sqlite3.connect("tichu.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY,
    name TEXT           
)
""")

conn.commit()

conn.close()