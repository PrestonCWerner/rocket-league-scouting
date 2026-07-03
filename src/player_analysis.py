import pandas as pd
import streamlit as st
import duckdb
import datetime
from pathlib import Path

@st.cache_data
def load_data(csv_to_report: str) -> pd.DataFrame:
   return pd.read_csv(csv_to_report)

@st.cache_data
def show_data(raw_data: pd.DataFrame) -> None:
    with st.container():
        st.subheader("Game Data Overview", text_alignment = "center")
        st.dataframe(raw_data)

@st.cache_data
def show_metrics(raw_data: pd.DataFrame) -> None:
    with st.container():
        st.subheader("Per-Game Statistics", text_alignment = "center")
        gpg, apg, svpg, scorepg = st.columns(4)
        
        avg_query = "SELECT AVG(goals)::DECIMAL(4,2) AS avg_goals, AVG(assists)::DECIMAL(4,2) AS avg_assists, AVG(saves)::DECIMAL(4,2) AS avg_saves, AVG(score)::DECIMAL(6,2) AS avg_score FROM raw_data"
        avg_df = duckdb.sql(avg_query).df()

        gpg.metric(label = "**GOALS PER GAME**", value = avg_df.iloc[0]["avg_goals"], border = True)
        apg.metric(label = "**ASSISTS PER GAME**", value = avg_df.iloc[0]["avg_assists"], border = True)
        svpg.metric(label = "**SAVES PER GAME**", value = avg_df.iloc[0]["avg_saves"], border = True)
        scorepg.metric(label = "**SCORE PER GAME**", value = avg_df.iloc[0]["avg_score"], border = True)

    

def show_win_loss(raw_dataL: pd.DataFrame) -> None:
    win_loss_query = "SELECT CAST(datetime AS DATETIME) AS date, match_result, COUNT(*) AS game_count FROM raw_data GROUP BY datetime, match_result ORDER BY datetime ASC"
    win_loss_df = duckdb.sql(win_loss_query).df()

    with st.container():
        st.subheader("Win-Loss Data", text_alignment = "center")

        start_date = win_loss_df.iloc[0]["date"].to_pydatetime()
        end_date = win_loss_df.tail(1).iloc[0]["date"].to_pydatetime()
        date_range = st.date_input(
            label="Select a date range",
            value=(start_date, end_date),
            min_value=start_date,
            max_value=end_date,
            format="MM.DD.YYYY",
        )
        if len(date_range) == 2:
            start_date, end_date = date_range
    
        
            mask = win_loss_df["date"].between(pd.to_datetime(start_date), pd.to_datetime(end_date))
            filtered_df = win_loss_df[mask]
            filtered_df["date"] = filtered_df["date"].dt.strftime("%m/%d")
        
            st.bar_chart(filtered_df, x = "date", y = "game_count", color = "match_result", stack = True)
        else:
            st.info("Please select both a start and end date.")

if __name__ == "__main__":
    dir = Path("./player_csvs/")
    files = sorted([f for f in dir.iterdir() if f.is_file()])

    st.set_page_config(layout = "wide")
    st.title("Rocket League Scouting Tool", text_alignment = "center")
    st.space("large")
    
    with st.sidebar:
        file_picker = st.radio(
            "Pick a file to analyze",
            files
        )

    raw_data: pd.DataFrame = load_data(file_picker)

    

    with st.container():
        metrics, data_overview, win_loss = st.columns(3)

        with metrics:
            show_metrics(raw_data)
        
        with data_overview:
            show_data(raw_data)

        with win_loss:
            show_win_loss(raw_data)
    
