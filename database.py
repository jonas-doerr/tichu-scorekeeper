import sqlite3
from scorekeeper import player

conn = sqlite3.connect("tichu.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY,
    name TEXT           
)
""")

def save_player(player): 
    cursor.execute(
        "INSERT INTO players(name) VALUES (?)",
        (player.name,)
    )

cursor.execute("SELECT * FROM players")

players = cursor.fetchall()

print(players)

conn.commit()

conn.close()