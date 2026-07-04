# Import necessary libraries
import os
import pandas as pd
import requests
import logging
from datetime import datetime


# Initiate global Logger
logger = logging.getLogger("player_replay_ingestion.py")
logger.setLevel(logging.DEBUG)

def initiate_logger() -> None:
    # Clear logger handlers, if any exist
    logger.handlers.clear()
    
    # Define log message format
    console_formatter = logging.Formatter('%(levelname)s: ON LINE %(lineno)d - %(message)s')
    file_formatter = logging.Formatter(
        fmt="%(levelname)s: at %(asctime)s on line %(lineno)d in %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO) 
    console_handler.setFormatter(console_formatter)

    # Create file handler
    file_handler = logging.FileHandler("./.logs/player_replay_ingestion.log", mode="w")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    # Connect handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.info("Logger initiated successfully.")
   

def verify_raw_source_data(raw_source: pd.DataFrame) -> bool:
    #TODO: add assertions and such for data validation
    assert (raw_source['goals'] <= 10).all(), logger.DEBUG("Expected goals above range")

    return True
    

def parse_player_match_info(replay_json: dict, player_name: str, team_goals: dict) -> pd.DataFrame:
    # Parses individual game stats
    # Returns Data Frame with single row representing game stats

    replay_id: str = replay_json["id"]
    playlist: str = replay_json["match_type"]
    match_type: str = replay_json["team_size"]
    date = pd.to_datetime(replay_json["date"])
    
    match_won: bool = False
    player_index: int = None
    player_team: str = None
    opponent_team: str = None
    goals_for: int = None
    goals_against: int = None

    for index, player in enumerate(replay_json["blue"]["players"]):
        if player["name"] == player_name:
            player_team = "blue"
            opponent_team = "orange"
            player_index = index
            break
    
    if player_team is None:
        for index, player in enumerate(replay_json["orange"]["players"]):
            if player["name"] == player_name:
                player_team = "orange"
                opponent_team = "blue"
                player_index = index
                break
    
    if player_team is None:
        return pd.DataFrame({})

    platform: str = replay_json[player_team]["players"][player_index]["id"]["platform"]
    car_name: str = replay_json[player_team]["players"][player_index]["car_name"]

    
    goals_for = team_goals[player_team]
    goals_against = team_goals[opponent_team]

    if player_team == "orange":
        if team_goals["orange"] > team_goals["blue"]:
            match_won = True
    elif player_team == "blue":
        if team_goals["blue"] > team_goals["orange"]:
            match_won = True
    
    stat_dict: dict = replay_json[player_team]["players"][player_index]["stats"]["core"]
    movement_dict: dict = replay_json[player_team]["players"][player_index]["stats"]["movement"]
    boost_dict: dict = replay_json[player_team]["players"][player_index]["stats"]["boost"]
    positioning_dict: dict = replay_json[player_team]["players"][player_index]["stats"]["positioning"]
    base_dict: dict = { "replay_id": replay_id, "datetime": date, "platform": platform, "car_name": car_name,  "playlist": playlist, "match_type": match_type, "match_result": "W" if match_won else "L", "team_goals": goals_for, "opp_goals": goals_against }
    result_dict: dict = base_dict | stat_dict | movement_dict | boost_dict | positioning_dict

    resultant_frame = pd.DataFrame([result_dict])

    resultant_frame = resultant_frame.astype({
        "playlist": str,
        "match_type": str,
        "match_result": str,
        "shots": int,
        "shots_against": int,
        "saves": int,
        "assists": int,
        "score": int, 
        "mvp": bool, 
        "shooting_percentage": float
    })

    return resultant_frame

    

def get_raw_data(player_name: str, game_count: int, api_auth_key: str) -> pd.DataFrame:
    # Ingests raw data into a Data Frame for transformation at a later step.
    # Output is a Data Frame where each row is an individual game performance by the selected player.

    AUTH_HEADER = {"Authorization": api_auth_key}

    resultant_frame = pd.DataFrame()

    try:
        # Get replays overview data
        replays_overview_data = requests.get("https://ballchasing.com/api/replays" + f"?player-name={player_name}&count={game_count}", headers = AUTH_HEADER)


        if not replays_overview_data.json()['list']:
            error_dict = {"error" : ["Player does not exist."]}
            return pd.DataFrame(error_dict)

    except requests.exceptions.Timeout as e:
        logger.error(f"API request timed out: {e}")
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Network problem or connection refused: {e}")
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred (e.g., 404 or 500): {e}")
    except requests.exceptions.RequestException as e:
        logger.error(f"An ambiguous error occurred while handling the request: {e}")
    
    # Get replay list to iterate through.
    replays_list: list = replays_overview_data.json()["list"]

    try:
        for replay in replays_list:
            replay_data = requests.get("https://ballchasing.com/api/replays" + f"/{replay["id"]}", headers = AUTH_HEADER)
            orange_goals: int = 0
            blue_goals: int = 0
            try:
                orange_goals = replay["orange"]["goals"]
                blue_goals = replay["blue"]["goals"]
            except KeyError as e:
                logger.info("One team went goalless.")

            resultant_frame = pd.concat([resultant_frame, parse_player_match_info(replay_data.json(), player_name, {"orange": orange_goals, "blue": blue_goals})], ignore_index = True)
    
    except requests.exceptions.Timeout as e:
        logger.error(f"API request timed out: {e}")
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Network problem or connection refused: {e}")
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred (e.g., 404 or 500): {e}")
    except requests.exceptions.RequestException as e:
        logger.error(f"An ambiguous error occurred while handling the request: {e}")
    
    resultant_frame.reset_index(inplace=True)

    return resultant_frame

def ingest_data(player_name: str, game_count: int, api_auth_key: str) -> pd.DataFrame:
    initiate_logger()
    
    raw_frame: pd.DataFrame = get_raw_data(player_name, game_count, api_auth_key)

    if "error" in raw_frame.columns:
        return raw_frame
    else:
        assert verify_raw_source_data(raw_frame), logging.critical("Raw DataFrame could not be verified; see log for details.")

    logging.shutdown()

    return raw_frame


