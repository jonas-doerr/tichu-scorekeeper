import sqlite3
from scorekeeper import Player

conn = sqlite3.connect("tichu.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE           
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY,
    date TEXT,
    winner TEXT,
    score1 INTEGER,
    score2 INTEGER
)
""")

def save_player(player): 
    conn = sqlite3.connect("tichu.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO players(name) VALUES (?)",
        (player.name,)
    )

    conn.commit()
    conn.close()

def save_game(date, winner, score1, score2):
    conn = sqlite3.connect("tichu.db")
    cursor = conn.cursor()

    cursor.execute(
        """INSERT INTO games(date, winner, score1, score2) 
        VALUES (?, ?, ?, ?)""",
        (date, winner, score1, score2)
    )

    conn.commit()
    conn.close()

def commit():
    conn.commit()

def close():
    conn.close()

def view_games():
    conn = sqlite3.connect("tichu.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM games")

    for game in cursor.fetchall():
        print(game)

    conn.close()

cursor.execute("SELECT * FROM players")

players = cursor.fetchall()

print(players)

conn.commit()

conn.close()