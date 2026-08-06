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

#Games Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY,
    date TEXT,
    score1 INTEGER,
    score2 INTEGER
)
""")

game_id = cursor.lastrowid

#Rounds Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS rounds (
    id INTEGER PRIMARY KEY,
    game_id INTEGER,
    round_number INTEGER,
    score1 INTEGER,
    score2 INTEGER,
    one_two TEXT
)
""")

#Placements Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS placements (
    round_id INTEGER,
    player_id INTEGER,
    placement INTEGER,
    PRIMARY KEY (round_id, player_id)
)
""")

#Tichu Calls Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS calls (
    round_id INTEGER,
    player_id INTEGER,
    call_type TEXT,
    success INTEGER,
    PRIMARY KEY (round_id, player_id)
)
""")

def save_player(player): 
    conn = sqlite3.connect("tichu.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO players(name)
        VALUES (?)
        """,
        (player.name,)
    )

    cursor.execute(
        """
        SELECT id FROM players WHERE name = ?
        """,
        (player.name,)
    )

    player.id = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    return player.id

def save_game(date, score1, score2):
    conn = sqlite3.connect("tichu.db")
    cursor = conn.cursor()

    cursor.execute(
        """INSERT INTO games(date, score1, score2) 
        VALUES (?, ?, ?)""",
        (date, score1, score2)
    )

    conn.commit()
    conn.close()

def save_round(game_id, round_number, round):
    conn = sqlite3.connect("tichu.db")
    cursor = conn.cursor()

    cursor.execute(
        """INSERT INTO rounds(game_id, round_number, score1, score2, one_two) 
        VALUES (?, ?, ?, ?, ?)""",
        (game_id, round_number, round.score1, round.score2, round.one_two)
    )

    conn.commit()

    round_id = cursor.lastrowid

    conn.close()

    return round_id

def save_placements(round_id, round):
    conn = sqlite3.connect("tichu.db")
    cursor = conn.cursor()

    for placement, player in enumerate(round.finish_order, start=1):

        cursor.execute(
            """
            INSERT INTO placements(round_id, player_id, placement)
            VALUES (?, ?, ?)
            """,
            (round_id, player.id, placement)
        )

    conn.commit()
    conn.close()

def save_calls(round_id, round):
    conn = sqlite3.connect("tichu.db")
    cursor = conn.cursor()

    for player, call in round.calls.items():
        if call == 100:
            call_name = "Tichu"
        else:
            call_name = "Grand Tichu"
        if player == round.finish_order[0]:
            success = 1
        else:
            success = 0

        cursor.execute(
            """INSERT INTO calls(round_id, player_id, call_type, success) 
            VALUES (?, ?, ?, ?)""",
            (round_id, player.id, call_name, success)
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

def view_table(table_name):
    allowed_tables = [
        "players",
        "games",
        "rounds",
        "placements",
        "calls"
    ]

    if table_name not in allowed_tables:
        print("Invalid table name")
        return

    conn = sqlite3.connect("tichu.db")
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table_name}")

    rows = cursor.fetchall()

    print(f"\n--- {table_name} ---")

    for row in rows:
        print(row)

    conn.close()

cursor.execute("SELECT * FROM players")

players = cursor.fetchall()

print(players)

conn.commit()

conn.close()