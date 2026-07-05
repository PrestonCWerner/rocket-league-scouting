import pandas as pd
import streamlit as st
import duckdb
import datetime
from pathlib import Path

@st.cache_data
def load_data(csv_to_report: str) -> pd.DataFrame:
   # Caches raw csv data for further use
   return pd.read_csv(csv_to_report)

@st.cache_data
def show_data(raw_data: pd.DataFrame) -> None:
    # Generates tabular data from raw_data source
    with st.container():
        st.subheader("Game Data Overview", text_alignment = "center")
        st.dataframe(raw_data)

@st.cache_data
def show_positioning_data(raw_data: pd.DataFrame) -> None:
    with st.container():

        adtb_col, adtbp_col, adtbnp_col, adtm_col = st.columns(4)
        apdt_col,apnt_col, apot_col, apdh_col, apoh_col = st.columns(5)
        apbb_col, apib_col = st.columns(2)
        apmb_col, apmf_col, apctb_col, apffb_col = st.columns(4)
        

        avg_query = """
            SELECT
                AVG(avg_distance_to_ball) AS avg_distance_to_ball,
                AVG(avg_distance_to_ball_possession) AS avg_distance_to_ball_possession,
                AVG(avg_distance_to_ball_no_possession) AS avg_distance_to_ball_no_possession,
                AVG(avg_distance_to_mates) AS avg_distance_to_mates,
                AVG(percent_defensive_third) AS avg_pct_def_third,
                AVG(percent_offensive_third) AS avg_pct_off_third,
                AVG(percent_neutral_third ) AS avg_pct_neu_third,
                AVG(percent_defensive_half) AS avg_pct_def_half,
                AVG(percent_offensive_half) AS avg_pct_off_half,
                AVG(percent_behind_ball) AS avg_pct_behind_ball,
                AVG(percent_infront_ball) AS avg_pct_infront_ball,
                AVG(percent_most_back) AS avg_pct_most_back,
                AVG(percent_most_forward) AS avg_pct_most_forward,
                AVG(percent_closest_to_ball) AS avg_pct_closest_to_ball,
                AVG(percent_farthest_from_ball) AS avg_pct_farthest_from_ball
            FROM raw_data
        """

        avg_df = duckdb.sql(avg_query).df()

        adtb_col.metric(label = "**AVERAGE DISTANCE TO BALL**", value = avg_df.iloc[0]["avg_distance_to_ball"], border = True)
        adtbp_col.metric(label = "**AVERAGE DISTANCE TO BALL - POSSESSION**", value = avg_df.iloc[0]["avg_distance_to_ball_possession"], border = True)
        adtbnp_col.metric(label = "**AVERAGE DISTANCE TO BALL - OUT OF POSSESSION**", value = avg_df.iloc[0]["avg_distance_to_ball_no_possession"], border = True)
        adtm_col.metric(label = "**AVERAGE DISTANCE TO TEAMMATES**", value = avg_df.iloc[0]["avg_distance_to_mates"], border = True)

        apdt_col.metric(label = "**AVERAGE % OF TIME DEFENSIVE THIRD**", value = avg_df.iloc[0]["avg_pct_def_third"]/100, format = "percent", border = True)
        apnt_col.metric(label = "**AVERAGE % OF TIME NEUTRAL THIRD**", value = avg_df.iloc[0]["avg_pct_neu_third"]/100, format = "percent", border = True)
        apot_col.metric(label = "**AVERAGE % OF TIME OFFENSIVE THIRD**", value = avg_df.iloc[0]["avg_pct_off_third"]/100, format = "percent", border = True)
        apdh_col.metric(label = "**AVERAGE % OF TIME DEFENSIVE HALF**", value = avg_df.iloc[0]["avg_pct_def_half"]/100, format = "percent", border = True)
        apoh_col.metric(label = "**AVERAGE % OF TIME OFFENSIVE HALF**", value = avg_df.iloc[0]["avg_pct_off_half"]/100, format = "percent", border = True)

        apbb_col.metric(label = "**AVERAGE % OF TIME BEHIND BALL**", value = avg_df.iloc[0]["avg_pct_behind_ball"]/100, format = "percent", border = True)
        apib_col.metric(label = "**AVERAGE % OF TIME IN FRONT OF BALL**", value = avg_df.iloc[0]["avg_pct_infront_ball"]/100, format = "percent", border = True)

        apmb_col.metric(label = "**AVERAGE % OF TIME FURTHEST BACK**", value = avg_df.iloc[0]["avg_pct_most_back"]/100, format = "percent", border = True)
        apmf_col.metric(label = "**AVERAGE % OF TIME FURTHEST FORWARD**", value = avg_df.iloc[0]["avg_pct_most_forward"]/100, format = "percent", border = True)
        apctb_col.metric(label = "**AVERAGE % OF TIME CLOSEST TO BALL**", value = avg_df.iloc[0]["avg_pct_closest_to_ball"]/100, format = "percent", border = True)
        apffb_col.metric(label = "**AVERAGE % OF TIME FARTHEST FROM BALL**", value = avg_df.iloc[0]["avg_pct_farthest_from_ball"]/100, format = "percent", border = True)

@st.cache_data
def show_metrics(raw_data: pd.DataFrame) -> None:
    # Generate metrics data for core statistics

    with st.container():
        st.subheader("Core Statistics", text_alignment = "center")

        # Create columnar structure for the metrics cards
        win_col, mvp_col = st.columns(2)
        gpg, apg, svpg, scorepg = st.columns(4)
        shotpg, shot_pct_pg = st.columns(2)
        shots_against_pg, goals_against_pg = st.columns(2)
        
        # This query aggregates core statistics
        avg_query = """
            SELECT 
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

        # This query is counting the total number of MVPs achieved in the dataset
        mvp_query = """
            SELECT
                COUNT(mvp) AS total_mvps
            FROM raw_data
            WHERE mvp = TRUE
        """
        mvp_df = duckdb.sql(mvp_query).df()

        # This query is counting the total number of wins achieved in the dataset
        win_query = """
            SELECT
                match_result
            FROM raw_data
            WHERE match_result = 'W'
        """
        win_df = duckdb.sql(win_query).df()

        # Metrics are shown on cards for easier readability
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


@st.cache_data
def show_boost_data(raw_data: pd.DataFrame) -> None:
    # Generates boost data page, which shows key stats related to boost management and usage

    # This query averages a variety of boost stats
    boost_query = """
        SELECT
            AVG(bpm)::DECIMAL(5,2) AS avg_bpm,
            AVG(bcpm)::DECIMAL(5,2) AS avg_bcpm,
            AVG(avg_amount)::DECIMAL(5,2) AS avg_boost_amt,
            AVG(count_collected_big)::DECIMAL(6,2) AS avg_big_boost_collected,
            AVG(count_collected_small)::DECIMAL(6,2) AS avg_small_boost_collected,
            AVG(amount_overfill)::DECIMAL(5,2) AS avg_amt_overfill,
            AVG(amount_used_while_supersonic)::DECIMAL(6,2) AS avg_amount_used_supersonic,
            AVG(percent_zero_boost)::DECIMAL(5,2) AS avg_time_zero_boost,
            AVG(percent_full_boost)::DECIMAL(5,2) AS avg_time_full_boost,
            AVG(percent_boost_0_25)::DECIMAL(5,2) AS avg_time_0_25,
            AVG(percent_boost_25_50)::DECIMAL(5,2) AS avg_time_25_50,
            AVG(percent_boost_50_75)::DECIMAL(5,2) AS avg_time_50_75,
            AVG(percent_boost_75_100)::DECIMAL(5,2) AS avg_time_75_100
        FROM raw_data
    """
    boost_df = duckdb.sql(boost_query).df()

    # Create columnar structure for the metrics cards
    bpm_col, bcpm_col, avg_boost_amt_col = st.columns(3)
    avg_count_big_col_col, avg_count_small_col_col = st.columns(2)
    avg_amt_overfill_col, avg_amount_used_supersonic_col, avg_time_zero_col, avg_time_full_col = st.columns(4)
    avg_time_0_25_col, avg_time_25_50_col, avg_time_50_75_col, avg_time_75_100_col = st.columns(4)

    # Metrics are shown on cards for easier readability
    avg_boost_amt_col.metric(label = "**AVERAGE BOOST**", value = boost_df.iloc[0]["avg_boost_amt"], border = True)
    bpm_col.metric(label = "**AVERAGE BOOST USED PER MINUTE**", value = boost_df.iloc[0]["avg_bpm"], border = True)
    bcpm_col.metric(label = "**AVERAGE BOOST COLLECTED PER MINUTE**", value = boost_df.iloc[0]["avg_bcpm"], border = True)
    
    avg_count_big_col_col.metric(label = "**AVERAGE NUMBER OF BIG BOOST PADS COLLECTED**", value = boost_df.iloc[0]["avg_big_boost_collected"], border = True)
    avg_count_small_col_col.metric(label = "**AVERAGE NUMBER OF SMALL BOOST PADS COLLECTED**", value = boost_df.iloc[0]["avg_small_boost_collected"], border = True)

    avg_amt_overfill_col.metric(label = "AVERAGE AMOUNT OVERFILL", value = boost_df.iloc[0]["avg_amt_overfill"], border = True)
    avg_amount_used_supersonic_col.metric(label = "AVERAGE AMOUNT USED WHILE SUPERSONIC", value = boost_df.iloc[0]["avg_amount_used_supersonic"], border = True)
    avg_time_zero_col.metric(label = "AVERAGE % OF TIME WITH 0 BOOST", value = boost_df.iloc[0]["avg_time_zero_boost"]/100, format = "percent", border = True)
    avg_time_full_col.metric(label = "AVERAGE % OF TIME WITH FULL BOOST", value = boost_df.iloc[0]["avg_time_full_boost"]/100, format = "percent", border = True)

    avg_time_0_25_col.metric(label = "AVERAGE TIME WITH 0-25% BOOST", value = boost_df.iloc[0]["avg_time_0_25"]/100, format = "percent", border = True)
    avg_time_25_50_col.metric(label = "AVERAGE TIME WITH 25-50% BOOST", value = boost_df.iloc[0]["avg_time_25_50"]/100, format = "percent", border = True)
    avg_time_50_75_col.metric(label = "AVERAGE TIME WITH 50-75% BOOST", value = boost_df.iloc[0]["avg_time_50_75"]/100, format = "percent", border = True)
    avg_time_75_100_col.metric(label = "AVERAGE TIME WITH 75-100% BOOST", value = boost_df.iloc[0]["avg_time_75_100"]/100, format = "percent", border = True)


@st.cache_data
def show_movement_data(raw_data: pd.DataFrame) -> None:
    # Generates movement data metric cards

    # This query averages key movement stats
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

    # Create columnar structure for the metrics cards
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
    # Generates win-loss stacked bar chart, showing win-loss per day

    win_loss_query = "SELECT CAST(datetime AS DATETIME) AS date, match_result, COUNT(*) AS game_count FROM raw_data GROUP BY datetime, match_result ORDER BY datetime ASC"
    win_loss_df = duckdb.sql(win_loss_query).df()
    win_loss_df["date"] = win_loss_df["date"].dt.strftime("%m/%d/%y")

    with st.container():
        st.subheader("Wins and Losses over Time", text_alignment = "center")
        st.bar_chart(win_loss_df, x = "date", y = "game_count", color = "match_result", stack = True)
       

if __name__ == "__main__":
    # If 'player_csvs/' is empty, return error message
    if len(st.session_state["df_manifest"]) == 0:
        print(st.session_state["df_manifest"])
        st.title(":red[No DataFrames are currently in the manifest. Please pull data from the 'pull data' page to populate this page.]")
    else:
        # Set page config layout. Components should occupy entirety of screen, hence "wide"
        st.set_page_config(layout = "wide")
        st.title(":blue[Rocket League Scouting Tool]", text_alignment = "center")
        
        # Sidebar tool for picking which CSV file to analyze
        with st.sidebar:
            df_picker = st.selectbox(
                "Pick a dataset to analyze",
                st.session_state["df_manifest"]
            )

        duckdb.register("cur_df", st.session_state["df_dict"][df_picker])

        # Create dataframe from raw csv based on the currently chosen CSV file name in the sidebar tool
        #cur_df: pd.DataFrame = load_data(st.session_state["df_dict"][""]
        # Drop unneccessary index column
        #cur_df.drop(columns = "index", inplace = True)

        # Create subheader container with subheader and game_type filter
        with st.container():
            subhead_col = st.columns(1)[0]
            game_type_col = st.columns(1)[0]

            # This allows global filtering by game type (1v1, 2v2, 3v3, 4v4)
            with game_type_col:
                game_type = st.radio(
                    "**FILTER BY GAME TYPE**",
                    ["All", "1v1", "2v2", "3v3", "4v4"],
                    horizontal = True
                )

                car_list = ["All"] + st.session_state["df_dict"][df_picker].sort_values(by = "car_name", ascending = True)["car_name"].unique().tolist()
                car_type = st.radio(
                    "**FILTER BY CAR**",
                    car_list,
                    horizontal = True
                )

            with subhead_col:
                cur_player_name = df_picker.split("_")[0]
                cur_game_count = len(st.session_state["df_dict"][df_picker])
                st.subheader(f"Currently viewing :green[{game_type}] stats for :green[{cur_player_name}] for the last :green[{cur_game_count}] games.", text_alignment = "center")

        
        # Create query to filter the data based on the game type chose in the radio widget
        game_dict_converter:dict = {"All": "", "1v1": "AND match_type = 1", "2v2": "AND match_type = 2", "3v3": "AND match_type = 3", "4v4": "AND match_type = 4"}
        car_filter: str = "" if car_type == "All" else f"AND car_name = '{car_type}'"

        game_type_filter_query = f"""
            SELECT
                *
            FROM cur_df
            WHERE 1 = 1
            {game_dict_converter[game_type]}
            {car_filter}
        """

        filtered_df = duckdb.sql(game_type_filter_query).df()
        filtered_df.drop(columns="index", inplace=True)

        # If the filtered dataset is empty, alert user that the player has no games of that game type recorded in the provided dataset.
        if len(filtered_df) == 0:
            st.title(f"There are no games recorded for :red[{game_type}]. Please try a different game mode.")
        else:
            # Create tabular navigation to compartmentalize key, distinctive statistics: Core stats, Movement stats, and Boost stats.
            core_tab, movement_tab, boost_tab, positioning_tab = st.tabs(["**:green[CORE]**", "**:blue[MOVEMENT]**", "**:orange[BOOST]**", "**:yellow[POSITIONING]**"])
            with core_tab:
                with st.container():
                    metrics, data_overview, win_loss = st.columns(3)

                    with metrics:
                        show_metrics(filtered_df)
                    
                    with data_overview:
                        show_data(filtered_df)

                    with win_loss:
                        show_win_loss(filtered_df)
            
            with boost_tab:
                show_boost_data(filtered_df)
            
            with movement_tab:
                show_movement_data(filtered_df)
            
            with positioning_tab:
                show_positioning_data(filtered_df)
