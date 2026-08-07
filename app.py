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
        st.session_state.team1 = [
            Player(selected_players[0]),
            Player(selected_players[1])
        ]

        st.session_state.team2 = [
            Player(selected_players[2]),
            Player(selected_players[3])
        ]

        st.session_state.game = TichuGame(
            st.session_state.team1 + st.session_state.team2
        )

        st.success("Game started!")

if st.session_state.game:

    game = st.session_state.game

    st.write(
        f"Score: {game.score1} - {game.score2}"
    )

    team1_score = st.slider(
        "Team 1 score",
        min_value=-25,
        max_value=125,
        value=50,
        step=5
    )

    team2_score = 100 - team1_score
    st.write(f"{team1_score} to {team2_score}")

    #Create Finish Order
    players = st.session_state.team1 + st.session_state.team2
    st.subheader("Finish Order")
    finish_order = []
    available_players = players.copy()

    for place in range(1, 5):
        selected = st.selectbox(
            f"{place}st" if place == 1 else f"{place}th",
            available_players,
            format_func=lambda player: player.name,
            key=f"finish_{place}"
        )

        finish_order.append(selected)

        available_players = [
            player for player in available_players
            if player.name != selected.name
        ]

    st.write("Finish order:", [player.name for player in finish_order])

    col1, col2 = st.columns(2)

    #Record any Tichus
    with col1:
        for player in st.session_state.team1:
            call = st.radio(
                player.name,
                ["None", "Tichu", "Grand Tichu"],
                key=f"{player.name}_call",
                horizontal=True
            )

    with col2:
            for player in st.session_state.team2:
                call = st.radio(
                    player.name,
                    ["None", "Tichu", "Grand Tichu"],
                    key=f"{player.name}_call",
                    horizontal=True
                )

    calls = {}

    for player in st.session_state.team1 + st.session_state.team2:
        call = st.session_state[f"{player.name}_call"]

        if call == "Tichu":
            calls[player] = 100
        elif call == "Grand Tichu":
            calls[player] = 200

    if st.button("Add Round"):

        round_data = Round(
            team1_score,
            team2_score,
            finish_order,
            calls,
            st.session_state.team1,
            st.session_state.team2
        )

        game.add_round(round_data)

        st.success("Round added")