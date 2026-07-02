# Import necessary libraries
import os
import pandas as pd
import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()
API_AUTH_KEY = os.getenv("API_AUTHORIZATION_KEY")
AUTH_HEADER = {"Authorization": API_AUTH_KEY}
BASE_URL = os.getenv("BASE_URL")

def verify_raw_source_data(raw_source: pd.DataFrame) -> bool:
    print("Hi!")

def parse_player_match_info(replay_json: dict, player_name: str) -> pd.DataFrame:
    # Parses individual game stats
    # Returns Data Frame with single row representing game stats
    
    playlist: str = replay_json["playlist_id"]
    date = pd.to_datetime(replay_json["date"])
    
    
    player_team: str = ""
    player_index: int = None

    for index, player in enumerate(replay_json["blue"]["players"]):
        if player["name"] == player_name:
            player_team = "blue"
            player_index = index
            break
    
    if (player_team == ""):
        for index, player in enumerate(replay_json["orange"]["players"]):
            if player["name"] == player_name:
                player_team = "orange"
                player_index = index
                break
    
    stat_dict: dict = replay_json[player_team]["players"][index]["stats"]["core"]
    base_dict: dict = { "playlist": playlist, "datetime": date, "team": "home" if player_team == "blue" else "away" }
    result_dict: dict = base_dict | stat_dict

    resultant_frame = pd.DataFrame([result_dict])
    
    return resultant_frame

    

def get_raw_data(player_name: str, game_count: int) -> pd.DataFrame:
    # Ingests raw data into a Data Frame for transformation at a later step.
    # Output is a Data Frame where each row is an individual game performance by the selected player.

    resultant_frame = pd.DataFrame()

    try:
        # Get replays overview data
        replays_overview_data = requests.get(BASE_URL + f"?player-name={player_name}&count={game_count}", headers = AUTH_HEADER)

    except requests.exceptions.Timeout as e:
        print(f"The request timed out: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"Network problem or connection refused: {e}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred (e.g., 404 or 500): {e}")
    except requests.exceptions.RequestException as e:
        print(f"An ambiguous error occurred while handling the request: {e}")
    
    # Get replay list to iterate through.
    replays_list: list = replays_overview_data.json()["list"]

    try:
        for replay in replays_list:
            replay_data = requests.get(BASE_URL + f"/{replay["id"]}", headers = AUTH_HEADER)
            resultant_frame = pd.concat([resultant_frame, parse_player_match_info(replay_data.json(), player_name)], ignore_index = True)
    
    except requests.exceptions.Timeout as e:
        print(f"The request timed out: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"Network problem or connection refused: {e}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred (e.g., 404 or 500): {e}")
    except requests.exceptions.RequestException as e:
        print(f"An ambiguous error occurred while handling the request: {e}")

    

    return resultant_frame

if __name__ == "__main__":
    # Get the player to analyze and number of games to analyze
    # Validate that name and count are of correct types
    name_flagged: bool = True
    count_flagged: bool = True
    player_name: str = ""
    game_count: int = 0

    while (name_flagged or count_flagged):
        if name_flagged:
            player_name = input("Enter the player's name: ")
        
        if count_flagged:
            game_count = input("Enter number of games to analyze: ")

        name_flagged = False
        count_flagged = False

        if (not isinstance(player_name, str)):
            print(f"{player_name} is not a valid input. Input was of type {type(player_name)}, where type str was expected.")
            name_flagged = True
        try:
            game_count = int(game_count)
        except ValueError:
           print(f"{game_count} is not a valid input. Input was of type {type(game_count)}, where type int was expected.")
           count_flagged = True
    
    raw_frame = get_raw_data(player_name, game_count)
    print(raw_frame.head())


