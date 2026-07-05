import requests
import pandas as pd

if __name__ == "__main__":
    replay_data = requests.get("https://ballchasing.com/api/replays/e9c65df6-9d8a-49e8-a4c3-5a2295e5f083", headers = {"Authorization": "sXipbcDg9SexNWpqktZ6syDBh3Cj0WJNe4tX0JGk"})
    print(replay_data.json())