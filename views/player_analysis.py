import pandas as pd
import streamlit as st
import duckdb
import datetime
import altair as alt
from pathlib import Path

@st.cache_data
def show_core_data(raw_data: pd.DataFrame) -> None:
    """ Generates table form for general statistics. """

    with st.container():
        st.subheader("Game Data Overview", text_alignment = "center")
        st.dataframe(raw_data)

@st.cache_data
def show_positioning_data(raw_data: pd.DataFrame) -> None:
    """ Generates container for displaying positioning data. Additionally transforms the raw DataFrame into and aggregated DataFrame. """
    with st.container():

        adtb_col, adtbp_col, adtbnp_col, adtm_col = st.columns(4)
        apdt_col,apnt_col, apot_col, apdh_col, apoh_col = st.columns(5)
        apbb_col, apib_col = st.columns(2)
        apmb_col, apmf_col, apctb_col, apffb_col = st.columns(4)
        

        avg_query = """
            SELECT
                AVG(avg_distance_to_ball)::DECIMAL(6,2) AS avg_distance_to_ball,
                AVG(avg_distance_to_ball_possession)::DECIMAL(6,2) AS avg_distance_to_ball_possession,
                AVG(avg_distance_to_ball_no_possession)::DECIMAL(6,2) AS avg_distance_to_ball_no_possession,
                AVG(avg_distance_to_mates)::DECIMAL(6,2) AS avg_distance_to_mates,
                AVG(percent_defensive_third)::DECIMAL(5,2) AS avg_pct_def_third,
                AVG(percent_offensive_third)::DECIMAL(5,2) AS avg_pct_off_third,
                AVG(percent_neutral_third )::DECIMAL(5,2) AS avg_pct_neu_third,
                AVG(percent_defensive_half)::DECIMAL(5,2)  AS avg_pct_def_half,
                AVG(percent_offensive_half)::DECIMAL(5,2)  AS avg_pct_off_half,
                AVG(percent_behind_ball)::DECIMAL(5,2)  AS avg_pct_behind_ball,
                AVG(percent_infront_ball)::DECIMAL(5,2)  AS avg_pct_infront_ball,
                AVG(percent_most_back)::DECIMAL(5,2)  AS avg_pct_most_back,
                AVG(percent_most_forward)::DECIMAL(5,2)  AS avg_pct_most_forward,
                AVG(percent_closest_to_ball)::DECIMAL(5,2)  AS avg_pct_closest_to_ball,
                AVG(percent_farthest_from_ball)::DECIMAL(5,2) AS avg_pct_farthest_from_ball
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
def show_core_metrics(raw_data: pd.DataFrame) -> None:
    """ Generates container for displaying core data. Additionally transforms the raw DataFrame into and aggregated DataFrame. """

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
                AVG(shooting_percentage)::DECIMAL(5,2) AS avg_shooting_pct,
                AVG(shots_against)::DECIMAL(5,2) AS avg_shots_against,
                AVG(goals_against)::DECIMAL(5,2) AS avg_goals_against
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
    """ Generates boost data report, transforming the raw_data DataFrame into an aggregated DataFrame """

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
    """ Generates boost data report, transforming the raw_data DataFrame into an aggregated DataFrame. """

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
    """ Generates win-loss graph on Core tab. """

    win_loss_query = "SELECT CAST(datetime AS DATETIME) AS date, match_result, COUNT(*) AS game_count FROM raw_data GROUP BY datetime, match_result ORDER BY datetime ASC"
    win_loss_df = duckdb.sql(win_loss_query).df()
    win_loss_df["date"] = win_loss_df["date"].dt.strftime("%m/%d/%y")

    with st.container():
        st.subheader("Wins and Losses over Time", text_alignment = "center")

        color_scale = alt.Scale(
            domain=["W", "L"],
            range=['#2ecc71', '#e74c3c']  # True = Green, False = Red
        )

        chart = alt.Chart(win_loss_df).mark_bar().encode(
            x= alt.X('date:N', axis=alt.Axis(labelAngle=-45)),
            y= alt.Y('game_count:Q', title = "Game Count", axis=alt.Axis(tickMinStep=1)),
            color=alt.Color('match_result:N', scale=color_scale, title='Match Result')
        )

        # 4. Render in Streamlit
        st.altair_chart(chart, use_container_width=True)

def filter_df() -> pd.DataFrame:
    """ Creates container for multiple filters and applies those filters to the current selected DataFrame. """

    with st.container():
            subhead_col = st.columns(1)[0]
            game_type_col, car_type_col, playlist_col, game_count_col = st.columns(4)

            # This allows global filtering by game type (1v1, 2v2, 3v3, 4v4)
            with game_type_col:
                game_type = st.radio(
                    label = "**FILTER BY GAME TYPE**",
                    options = ["All", "1v1", "2v2", "3v3", "4v4"],
                    horizontal = True
                )

                st.session_state["game_type"] = game_type

            # This radio allows global filtering on car type
            with car_type_col:
                car_list = ["Any"] + st.session_state["df_dict"][df_picker].sort_values(by = "car_name", ascending = True)["car_name"].unique().tolist()
                car_type = st.radio(
                    label = "**FILTER BY CAR**",
                    options = car_list,
                    horizontal = True
                )

                st.session_state["car_type"] = car_type
            
            with playlist_col:
                playlist_list = ["All"] + st.session_state["df_dict"][df_picker].sort_values(by = "playlist", ascending = True)["playlist"].unique().tolist()
                playlist_type = st.radio(
                    label = "**FILTER BY PLAYLIST**",
                    options = playlist_list,
                    horizontal = True
                )

                st.session_state["playlist"] = playlist_type
            
            with game_count_col:
                game_count_list = [i for i in range(1, len(st.session_state["df_dict"][df_picker]) + 1)]
                game_count_picker = st.selectbox(
                    label = "**FILTER BY GAME COUNT**",
                    options = game_count_list,
                    index = len(st.session_state["df_dict"][df_picker])-1
                )

                st.session_state["game_count"] = game_count_picker


            # Create query to filter the data based on the game type chose in the radio widget
            game_dict_converter:dict = {"All": "", "1v1": "AND match_type = 1", "2v2": "AND match_type = 2", "3v3": "AND match_type = 3", "4v4": "AND match_type = 4"}
            car_filter: str = "" if car_type == "Any" else f"AND car_name = '{car_type}'"
            playlist_filter: str = "" if playlist_type == "All" else f"AND playlist = '{playlist_type}'"

            game_type_filter_query = f"""
                SELECT
                    *
                FROM cur_df
                WHERE 1 = 1
                {game_dict_converter[game_type]}
                {car_filter}
                {playlist_filter}
            """

            filtered_df = duckdb.sql(game_type_filter_query).df()
            filtered_df.drop(columns="index", inplace=True)
            filtered_df = filtered_df.sort_values(by = "datetime", ascending = False).head(game_count_picker)
            st.session_state["filtered_df"] = filtered_df


            with subhead_col:
                st.subheader(f"Currently viewing :green[{st.session_state["game_type"]}] stats for :green[{df_picker}] for the last :green[{len(filtered_df)}] games.", text_alignment = "center")
    
    

    return filtered_df

if __name__ == "__main__":
    """ Generates page for data reporting. """
    
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

        filtered_df = filter_df()

        # If the filtered dataset is empty, alert user that the player has no games of that game type recorded in the provided dataset.
        if len(filtered_df) == 0:
            st.title(f"There are no games recorded for :red[{st.session_state["game_type"]}] game mode using :red[{st.session_state["car_type"]}] car in the last :red[{st.session_state["game_count"]}] games. Please try a different game mode, car, and/or number of games.")
        else:
            # Create tabular navigation to compartmentalize key, distinctive statistics: Core stats, Movement stats, and Boost stats.
            core_tab, movement_tab, boost_tab, positioning_tab = st.tabs(["**:green[CORE]**", "**:blue[MOVEMENT]**", "**:orange[BOOST]**", "**:yellow[POSITIONING]**"])
            with core_tab:
                with st.container():
                    metrics, data_overview, win_loss = st.columns(3)

                    with metrics:
                        show_core_metrics(filtered_df)
                    
                    with data_overview:
                        show_core_data(filtered_df)

                    with win_loss:
                        show_win_loss(filtered_df)
            
            with boost_tab:
                show_boost_data(filtered_df)
            
            with movement_tab:
                show_movement_data(filtered_df)
            
            with positioning_tab:
                show_positioning_data(filtered_df)
