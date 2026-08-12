import streamlit as st
import pandas as pd
from database import view_games, get_players
from scorekeeper import Player
from simulation import simulate_game

st.subheader("Past Games")

games = view_games()

if games:
    df = pd.DataFrame(
        games,
        columns=["Game ID", "Date", "Team 1", "Team 2"]
    )
    st.dataframe(
        df,
        hide_index=True
    )
else:
    st.write("No games recorded yet.")

#Simulate games
st.header("Simulate Games")
database_players = get_players()

if "simulated_players" not in st.session_state:
    st.session_state.simulated_players = None
if "simulation_message" not in st.session_state:
    st.session_state.simulation_message = None

if st.session_state.simulation_message:
    st.success(st.session_state.simulation_message)
    st.session_state.simulation_message = None

player_objects = []

for id, name in database_players:
    player = Player(name, id)
    player_objects.append(player)

database_names = [player.name for player in player_objects]

st.session_state.simulated_players = st.multiselect(
    "Choose 4 players (First 2 are team 1, second 2 are on team 2)",
    player_objects,
    format_func=lambda player: player.name
)

game_number = st.number_input("Number of games to simulate", min_value = 1, max_value = 20)

if st.button("Simulate New Game"):

    if len(st.session_state.simulated_players) != 4:
        st.warning("Please choose exactly 4 players")

    elif game_number < 1 or game_number > 20:
        st.warning("Please choose between 1 and 20 games")

    else:
        for _ in range(game_number):
            simulate_game(st.session_state.simulated_players)

        st.session_state.simulation_message = (f"Simulated {game_number} game(s).")

        st.rerun()