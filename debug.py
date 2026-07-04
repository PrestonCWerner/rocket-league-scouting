import requests
import pandas as pd

if __name__ == "__main__":
    player_name = "John"
    game_count = "1"
    req = requests.get("https://ballchasing.com/api/replays" + f"?player-name={player_name}&count={game_count}", headers = {"Authorization": "sXipbcDg9SexNWpqktZ6syDBh3Cj0WJNe4tX0JGk"})

    for replay in req.json()['list']:
            replay_data = requests.get("https://ballchasing.com/api/replays" + f"/{replay["id"]}", headers = {"Authorization": "sXipbcDg9SexNWpqktZ6syDBh3Cj0WJNe4tX0JGk"})
            print(replay["orange"]["players"][2]["id"]["platform"])
            for index, player in enumerate(replay["orange"]["players"]):
                print(player["name"])
                print(index)