import pandas as pd
import streamlit as st

if __name__ == "__main__":
    raw_data = pd.read_csv("./player_csvs/Scouting_Report_Charlemagne-2026_07_02-17_40_37")
    st.dataframe(raw_data)