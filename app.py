import streamlit as st

from scorekeeper import Player, Round, TichuGame
from database import save_game, save_round, save_placements, save_calls, get_players


st.title("Tichu Scorekeeper")

#Fetch player list from database
players = get_players()

names = [player[1] for player in players]

selected_players = st.multiselect(
    "Choose 4 players",
    names
)

#Save memory
if "game" not in st.session_state:
    st.session_state.game = None

if st.button("Start Game"):

    if len(selected_players) != 4:
        st.warning("Choose 4 players")

    else:
        team1 = [
            Player(selected_players[0]),
            Player(selected_players[1])
        ]

        team2 = [
            Player(selected_players[2]),
            Player(selected_players[3])
        ]

        st.session_state.game = TichuGame(
            team1 + team2
        )

        st.success("Game started!")

if st.session_state.game:

    game = st.session_state.game

    st.write(
        f"Score: {game.score1} - {game.score2}"
    )

    team1_score = st.number_input(
        "Team 1 score",
        value=50
    )

    team2_score = st.number_input(
        "Team 2 score",
        value=50
    )

    if st.button("Add Round"):

        round_data = Round(
            team1_score,
            team2_score,
            [],
            {}
        )

        game.add_round(round_data)

        st.success("Round added")