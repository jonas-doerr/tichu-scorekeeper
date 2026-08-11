import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_players, get_player_placements, get_games_played, get_player_calls
from analysis import placement_list, call_stats, count_one_two


st.title("Player Statistics")

if "selected_player_id" not in st.session_state:
    st.session_state.selected_player_id = None

players = get_players()

if players:
    df = pd.DataFrame(
        players,
        columns=["Player ID", "Name"]
    )
    st.dataframe(
        df,
        hide_index=True
    )
else:
    st.write("No players recorded yet.")

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

placement_counts, average_placement = placement_list(st.session_state.selected_player_id)

labels = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th"}
df = pd.DataFrame(
    [
        {"Placement": labels[place], "Count": count}
        for place, count in placement_counts.items()
    ]
)

col1, col2 = st.columns(2)

with col1:
    games_played = get_games_played(st.session_state.selected_player_id)
    st.metric("Games Played", games_played)

with col2:
    st.metric("Average Placement", f"{average_placement:.2f}")

st.subheader(f"{selected_name}'s Placements")
st.bar_chart(df, x="Placement", y="Count")

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