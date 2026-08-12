import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_players, get_player_placements, get_games_played, get_player_calls, save_player
from analysis import placement_list, call_stats, count_one_two, games_won
from scorekeeper import Player


st.title("Player Statistics")

if "selected_player_id" not in st.session_state:
    st.session_state.selected_player_id = None

if "creating_player" not in st.session_state:
    st.session_state.creating_player = False

if st.button("Add Player"):
    st.session_state.creating_player = True

if st.session_state.creating_player:
    name = st.text_input("Player Name")
    if st.button("Create New Player"):
        if name != None:
            new_player = Player(name)
            save_player(new_player)
            st.session_state.creating_player = False
            st.rerun()
    else:
        st.warning("Please input a player name")

players = get_players()

player_dict = {
    name: player_id
    for player_id, name in players
}

selected_name = st.selectbox(
    "Choose a player",
    list(player_dict.keys())
)

st.session_state.selected_player_id = player_dict[selected_name]

st.write("Player ID:", st.session_state.selected_player_id)

try:
    placement_counts, average_placement = placement_list(st.session_state.selected_player_id)

    labels = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th"}
    df = pd.DataFrame(
        [
            {"Placement": labels[place], "Count": count}
            for place, count in placement_counts.items()
        ]
    )

    col1, col2, col11, col12 = st.columns(4)

    with col1:
        games_played = get_games_played(st.session_state.selected_player_id)
        st.metric("Games Played", games_played)

    with col2:
        st.metric("Average Placement", f"{average_placement:.2f}")

    win_rate, avg_score_diff = games_won(st.session_state.selected_player_id)
    with col11:
        st.metric("Win Rate", f"{100 * win_rate:.1f}%")

    with col12:
        st.metric("Average Score Difference", f"{avg_score_diff:.0f}")

    st.subheader(f"{selected_name}'s Placements")
    st.bar_chart(df, x="Placement", y="Count")

except ZeroDivisionError:
    st.warning("No games played by this player")

tichus, grand_tichus, successful_tichus, successful_grand_tichus = call_stats(st.session_state.selected_player_id)

st.subheader("Tichu Call Statistics")

col3, col4, col5, col6 = st.columns(4)

with col3:
    st.metric("Tichus Called", len(tichus))
with col4:
    st.metric("Tichu Success Rate",
            f"{len(successful_tichus) / len(tichus) * 100:.1f}%"
            if tichus else "N/A")
with col5:
    st.metric("Grand Tichus Called", len(grand_tichus))
with col6:
    st.metric("Grand Tichu Success Rate",
            f"{len(successful_grand_tichus) / len(grand_tichus) * 100:.1f}%"
            if grand_tichus else "N/A")

df = pd.DataFrame({
    "Type": ["Tichu", "Grand Tichu"],
    "Called": [len(tichus), len(grand_tichus)],
    "Successful": [
        len(successful_tichus),
        len(successful_grand_tichus)
    ]
})

fig = px.bar(
    df,
    x="Type",
    y=["Called", "Successful"],
    barmode="group",
    title=f"{selected_name}'s Tichu Performance"
)

st.plotly_chart(fig, width='stretch')

one_twos_for, one_twos_against, total_rounds = count_one_two(st.session_state.selected_player_id)

st.subheader("1-2 Statistics")

col7, col8, col9, col10 = st.columns(4)

with col7:
    st.metric("1-2s for", one_twos_for)
with col8:
    st.metric("1-2s against", one_twos_against)
with col9:
    st.metric("Rounds with 1-2 for", f"{one_twos_for / total_rounds * 100:.1f}%"
                if total_rounds else "N/A")
with col10:
    st.metric("Rounds with 1-2 against",
            f"{one_twos_against / total_rounds * 100:.1f}%"
            if total_rounds else "N/A")