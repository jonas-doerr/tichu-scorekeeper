import streamlit as st
import pandas as pd
from database import view_games

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