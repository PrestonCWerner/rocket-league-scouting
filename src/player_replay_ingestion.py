# Import necessary libraries
import os
import pandas as pd
import requests
import logging
from datetime import datetime
from dotenv import load_dotenv

# Environment variable assignment for API Key and URL
load_dotenv()
API_AUTH_KEY = os.getenv("API_AUTHORIZATION_KEY")
AUTH_HEADER = {"Authorization": API_AUTH_KEY}
BASE_URL = os.getenv("BASE_URL")

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
    
    if (player_team is None):
        for index, player in enumerate(replay_json["orange"]["players"]):
            if player["name"] == player_name:
                player_team = "orange"
                opponent_team = "blue"
                player_index = index
                break
    
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
    base_dict: dict = { "replay_id": replay_id, "datetime": date, "playlist": playlist, "match_type": match_type, "match_result": "W" if match_won else "L", "team_goals": goals_for, "opp_goals": goals_against }
    result_dict: dict = base_dict | stat_dict | movement_dict | boost_dict

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

    

def get_raw_data(player_name: str, game_count: int) -> pd.DataFrame:
    # Ingests raw data into a Data Frame for transformation at a later step.
    # Output is a Data Frame where each row is an individual game performance by the selected player.

    resultant_frame = pd.DataFrame()

    try:
        # Get replays overview data
        replays_overview_data = requests.get(BASE_URL + f"?player-name={player_name}&count={game_count}", headers = AUTH_HEADER)

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
            replay_data = requests.get(BASE_URL + f"/{replay["id"]}", headers = AUTH_HEADER)
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

if __name__ == "__main__":
    initiate_logger()

    # Get the player to analyze and number of games to analyze
    # Validate that name and count are of correct types
    player_name: str = ""
    game_count: int = 0
    player_name_flag: bool = True
    game_count_flag: bool = True

    name_validation_list = [" ", "/", "\\", "<", ">", "\"", "\'"]

    while player_name_flag or game_count_flag:
        try:
            if player_name_flag:
                player_name = str(input("Please enter player name: "))
                
                for char in player_name:
                    if char in name_validation_list:
                        raise ValueError(f"Character '{char}' not accepted in player name.")
                if len(player_name) < 2 or len(player_name) > 32:
                    raise ValueError(f"Player name must be between 2 characters and 32 characters long.")

                player_name_flag = False
            
            if game_count_flag:
                game_count = int(input("Please enter game count for analysis: "))

                if game_count >= 50 or game_count < 1:
                    raise ValueError(f"Game count must be between 1 and 50 games.")

                game_count_flag = False
        
        except ValueError as e:
            logger.error(e)
    
    raw_frame: pd.DataFrame = get_raw_data(player_name, game_count)
    raw_frame.sort_values(by="datetime", ascending = True, inplace=True)

    assert verify_raw_source_data(raw_frame), logging.critical("Raw DataFrame could not be verified; see log for details.")

    

    first_datetime = raw_frame.head(1)["datetime"].iloc[0].strftime("%m_%d_%Y-%H_%M_%S")
    last_datetime = raw_frame.tail(1)["datetime"].iloc[0].strftime("%m_%d_%Y-%H_%M_%S")

    csv_path = f"./player_csvs/Scouting_Report_{player_name}-{first_datetime}__{last_datetime}"
    raw_frame.to_csv(csv_path, index=False)

    logger.info(f"Created csv file at {csv_path}.")


    logging.shutdown()


