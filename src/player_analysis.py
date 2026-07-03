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
        st.subheader("Core Statistics", text_alignment = "center")

        win_col, mvp_col = st.columns(2)
        gpg, apg, svpg, scorepg = st.columns(4)
        shotpg, shot_pct_pg = st.columns(2)
        shots_against_pg, goals_against_pg = st.columns(2)
        
        avg_query = """SELECT 
                            AVG(goals)::DECIMAL(4,2) AS avg_goals, 
                            AVG(assists)::DECIMAL(4,2) AS avg_assists, 
                            AVG(saves)::DECIMAL(4,2) AS avg_saves, 
                            AVG(score)::DECIMAL(6,2) AS avg_score, 
                            AVG(shots)::DECIMAL(4, 2) AS avg_shots, 
                            AVG(shooting_percentage)::DECIMAL(4,2) AS avg_shooting_pct,
                            AVG(shots_against)::DECIMAL(4,2) AS avg_shots_against,
                            AVG(goals_against)::DECIMAL(4,2) AS avg_goals_against
                        FROM raw_data"""
        avg_df = duckdb.sql(avg_query).df()

        mvp_query = """
            SELECT
                COUNT(mvp) AS total_mvps
            FROM raw_data
            WHERE mvp = TRUE
        """
        mvp_df = duckdb.sql(mvp_query).df()

        win_query = """
            SELECT
                COUNT(match_result) AS total_wins
            FROM raw_data
            WHERE match_result = 'W'
        """
        win_df = duckdb.sql(win_query).df()

        win_col.metric(label = "**WIN %**", value = len(win_df)/len(raw_data), format = "percent", border = True)
        mvp_col.metric(label = "Total MVPs", value = mvp_df.iloc[0]["total_mvps"], border = True)
        
        gpg.metric(label = "**GOALS PER GAME**", value = avg_df.iloc[0]["avg_goals"], border = True)
        apg.metric(label = "**ASSISTS PER GAME**", value = avg_df.iloc[0]["avg_assists"], border = True)
        svpg.metric(label = "**SAVES PER GAME**", value = avg_df.iloc[0]["avg_saves"], border = True)
        scorepg.metric(label = "**SCORE PER GAME**", value = avg_df.iloc[0]["avg_score"], border = True)

        shotpg.metric(label = "**SHOTS PER GAME**", value = avg_df.iloc[0]["avg_shots"], border = True)
        shot_pct_pg.metric(label = "**SHOOTING % PER GAME**", value = avg_df.iloc[0]["avg_shooting_pct"]/100, format = "percent", border = True)
        
        shots_against_pg.metric(label = "**SHOTS AGAINST PER GAME**", value = avg_df.iloc[0]["avg_shots_against"], border = True)
        goals_against_pg.metric(label = "**GOALS AGAINST PER GAME**", value = avg_df.iloc[0]["avg_goals_against"], border = True)



def show_boost_data(raw_data: pd.DataFrame) -> None:
    boost_query = """
        SELECT
            
    """

def show_movement_data(raw_data: pd.DataFrame) -> None:
    movement_query = """
        SELECT
            AVG(avg_speed)::DECIMAL(7,2) AS avg_speed,
            AVG(total_distance)::DECIMAL(9,2) AS avg_distance,
            AVG(percent_supersonic_speed)::DECIMAL(5,2) AS avg_supersonic,
            AVG(percent_boost_speed)::DECIMAL(5,2) AS avg_time_boost_speed,
            AVG(percent_slow_speed)::DECIMAL(5,2) AS avg_time_slow_speed,
            AVG(count_powerslide)::DECIMAL(5,2) AS avg_powerslide_count,
            AVG(percent_ground)::DECIMAL(5,2) AS avg_percent_ground,
            AVG(percent_low_air)::DECIMAL(5,2) AS avg_percent_low_air,
            AVG(percent_high_air)::DECIMAL(5,2) AS avg_percent_high_air
        FROM raw_data
    """

    movement_df = duckdb.sql(movement_query).df()

    speed_col, spatum_col = st.columns(2)
    supersonic_col, time_boost_speed_col, time_slow_speed_col = st.columns(3)
    ground_col, low_air_col, high_air_col, powerslide_col = st.columns(4)

    speed_col.metric(label = "**AVERAGE SPEED**", value = movement_df.iloc[0]["avg_speed"], format = "localized", border = True)
    spatum_col.metric(label = "**AVERAGE DISTANCE TRAVELLED**", value = movement_df.iloc[0]["avg_distance"], format = "localized", border = True)

    supersonic_col.metric(label = "**AVERAGE TIME SPENT SUPERSONIC**", value = movement_df.iloc[0]["avg_supersonic"]/100, format = "percent", border = True)
    time_boost_speed_col.metric(label = "**AVERAGE TIME SPENT BOOSTING**", value = movement_df.iloc[0]["avg_time_boost_speed"]/100, format = "percent", border = True)
    time_slow_speed_col.metric(label = "**AVERAGE TIME SPENT SLOW SPEED**", value = movement_df.iloc[0]["avg_supersonic"]/100, format = "percent", border = True)

    

    ground_col.metric(label = "**AVERAGE % OF TIME SPENT ON THE GROUND**", value = movement_df.iloc[0]["avg_percent_ground"]/100, format = "percent", border = True)
    low_air_col.metric(label = "**AVERAGE % OF TIME SPENT IN LOW AIR**", value = movement_df.iloc[0]["avg_percent_low_air"]/100, format = "percent", border = True)
    high_air_col.metric(label = "**AVERAGE % OF TIME SPENT IN HIGH AIR**", value = movement_df.iloc[0]["avg_percent_high_air"]/100, format = "percent", border = True)

    powerslide_col.metric(label = "**AVERAGE NUMBER OF POWERSLIDES**", value = movement_df.iloc[0]["avg_powerslide_count"], border = True)

@st.cache_data
def show_win_loss(raw_data: pd.DataFrame) -> None:
    win_loss_query = "SELECT CAST(datetime AS DATETIME) AS date, match_result, COUNT(*) AS game_count FROM raw_data GROUP BY datetime, match_result ORDER BY datetime ASC"
    win_loss_df = duckdb.sql(win_loss_query).df()
    win_loss_df["date"] = win_loss_df["date"].dt.strftime("%m/%d/%y")

    with st.container():
        st.subheader("Win-Loss Data", text_alignment = "center")
        st.bar_chart(win_loss_df, x = "date", y = "game_count", color = "match_result", stack = True)
       

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

    st.subheader(f"Currently viewing stats for {str(file_picker).split("_")[3].split("-")[0]} for last {len(raw_data)} games.", text_alignment = "center")

    core_tab, movement_tab, boost_tab = st.tabs(["Core", "Movement", "Boost"])
    
    with core_tab:
        with st.container():
            metrics, data_overview, win_loss = st.columns(3)

            with metrics:
                show_metrics(raw_data)
            
            with data_overview:
                show_data(raw_data)

            with win_loss:
                show_win_loss(raw_data)
    
    with boost_tab:
        show_boost_data(raw_data)
    
    with movement_tab:
        show_movement_data(raw_data)
