import streamlit as st

from scorekeeper import Player, Round, TichuGame
from database import save_game, save_round, save_placements, save_calls, get_players
from streamlit_sortables import sort_items

st.title("Tichu Scorekeeper")

if "game" not in st.session_state:
    st.session_state.game = None

if "team1" not in st.session_state:
    st.session_state.team1 = []

if "team2" not in st.session_state:
    st.session_state.team2 = []

if "game_id" not in st.session_state:
    st.session_state.game_id = None

#Fetch player list from database
database_players = get_players()


player_objects = []

for id, name in database_players:
    player = Player(name, id)
    player_objects.append(player)

database_names = [player.name for player in player_objects]

selected_players = st.multiselect(
    "Choose 4 players (First 2 are team 1, second 2 are on team 2)",
    database_names
)


#Begin the game when players are ready
if st.button("Start Game"):

    if len(selected_players) != 4:
        st.warning("Choose exactly 4 players")

    else:
        selected_players = [
            player
            for player in player_objects
            if player.name in selected_players
        ]

        st.session_state.players = selected_players

        st.session_state.team1 = [selected_players[:2]]
        st.session_state.team2 = [selected_players[2:]]

        st.session_state.game = TichuGame(
            selected_players
        )

        st.success("Game started!")

if st.session_state.game:

    game = st.session_state.game

    st.write(
        f"Score: {game.score1} - {game.score2}"
    )

    st.session_state.team1_score = st.slider(
        "Team 1 score",
        min_value=-25,
        max_value=125,
        value=50,
        step=5
    )

    st.session_state.team2_score = 100 - st.session_state.team1_score
    st.write(f"{st.session_state.team1_score} to {st.session_state.team2_score}")

    #Create Finish Order
    players = st.session_state.players
    st.subheader("Finish Order")

    # 1. Map names to Player objects
    player_map = {player.name: player for player in players}

    # 2. Extract string names so items is a list[str]
    player_names = [player.name for player in players]

    # 3. Pass list of strings to sort_items
    ordered_names = sort_items(player_names, direction="vertical")

    # 4. Convert string names back into Player objects
    st.session_state.finish_order = [player_map[name] for name in ordered_names]

    col1, col2 = st.columns(2)

    #Record any Tichus
    with col1:
        for player in st.session_state.players[:2]:
            call = st.radio(
                player.name,
                ["None", "Tichu", "Grand Tichu"],
                key=f"{player.id}_call",
                horizontal=True
            )

    with col2:
            for player in st.session_state.players[2:]:
                call = st.radio(
                    player.name,
                    ["None", "Tichu", "Grand Tichu"],
                    key=f"{player.id}_call",
                    horizontal=True
                )

    st.session_state.calls = {}

    for player in st.session_state.players:
        call = st.session_state[f"{player.id}_call"]

        if call == "Tichu":
            st.session_state.calls[player] = 100

        elif call == "Grand Tichu":
            st.session_state.calls[player] = 200

    if st.button("Add Round"):

        round_data = Round(
            st.session_state.team1_score,
            st.session_state.team2_score,
            st.session_state.finish_order,
            st.session_state.calls,
            st.session_state.team1,
            st.session_state.team2
        )

        game.add_round(round_data)

        st.success("Round added")

        st.rerun()

    if game.rounds:
        st.subheader("Rounds Played")

        for number, round_data in enumerate(game.rounds, start=1):
            st.write(
                f"Round {number}: "
                f"{round_data.score1}-{round_data.score2}"
            )