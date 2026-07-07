import streamlit as st
import pandas as pd
import requests
import time
from utils.player_replay_ingestion import ingest_data

@st.dialog("Ballchasing API Auth Key Submission", dismissible = False)
def set_api_auth_key() -> None:
    """ Generates a form for inputting user's API Auth key. """

    with st.form(key="api_key_submission", clear_on_submit=True):
        api_auth_key: str = st.text_input(label = "**ENTER AUTH KEY**", value=None, placeholder = "ABCDEFGHI12345678", type = "password", max_chars = 40, width = 200)
        submit_button = st.form_submit_button(label="Submit")
        close_window_button = st.form_submit_button(label="Close Window")

        if submit_button:
            if api_auth_key is None:
                st.error("Please put an API Auth Key in the text input.")
            elif not api_auth_key.isalnum():
                st.error("API Auth Key is not a valid key. Please double-check your Ballchasing API key.")
            elif len(api_auth_key) < 40:
                st.error(f"API Auth Key is not a valid key. Auth Key was of length {len(api_auth_key)} characters, but expected 40 characters. Please double-check your Ballchasing API key.")

            try:
                response = requests.get("https://ballchasing.com/api", headers = {
                    "Authorization": api_auth_key
                })

                if response.ok:
                    st.session_state["api_key"] = api_auth_key
                    tier: str = response.json()["type"]
                    st.success(f"API Authorization Key of tier '{tier}' added to this session.")
                else:
                    st.error(f"Error could not ping Ballchasing API. Status: {response.status_code}")
            except requests.exceptions.Timeout as e:
                st.error(f"API request timed out: {e}")
            except requests.exceptions.ConnectionError as e:
                st.error(f"Network problem or connection refused: {e}")
            except requests.exceptions.HTTPError as e:
                st.error(f"HTTP error occurred (e.g., 404 or 500): {e}")
            except requests.exceptions.RequestException as e:
                st.error(f"An ambiguous error occurred while handling the request: {e}")
        
        if close_window_button:
            st.rerun()

@st.dialog("Overwrite Existing Data?", dismissible = False)
def overwrite_popup(player_name: str, game_count: int) -> bool:
    """ Generates overwrite pop-up when user requests new data for existing player. """

    with st.form(key="overwrite_submission"):
        overwrite_choice = st.selectbox(
            label = f"** A dataframe already exists for player {player_name}. Would you like to overwrite the existing dataframe? **",
            options = [f"Overwrite data for {player_name}", f"Do not overwrite data for {player_name}"]
        )
        check = st.form_submit_button(label="Confirm")

        if check:
            if overwrite_choice == f"Overwrite data for {player_name}":
                st.success(f"Form submitted successfully. Pulling {player_name}'s Ballchasing data from the last {game_count} games!")
                add_df_to_list(player_name, game_count)
                time.sleep(5)
                st.rerun()
            else:
                st.success(f"Keeping existing data for {player_name}.")
                time.sleep(5)
                st.rerun()

def add_df_to_list(player_name: str, game_count: int):
    """ Creates DataFrame from ingested data based on player_name and game_count, then places DataFrame in DataFrame manifest and dictionary."""
    with st.spinner("Loading data..."):
        new_df: pd.DataFrame = ingest_data(player_name, game_count, st.session_state["api_key"])
        if "error" in new_df.columns:
            st.error(f"Last {game_count} games for player '{player_name}' could not be found.")
        else:
            new_df.sort_values(by="datetime", ascending = True, inplace=True)
            st.session_state["df_manifest"].append(f"{player_name}")
            st.session_state["df_dict"][f"{player_name}"] = new_df
            st.success(f"Successfully loaded data into DataFrame list.")


if __name__ == "__main__":
    """ Generates data ingestion page. """

    st.set_page_config(layout = "centered")
    with st.sidebar:
        if st.button("Clear Cache"):
            st.cache_data.clear()
        
        if st.button("Change API Authentication Key"):
            set_api_auth_key()

    if "api_key" in st.session_state:
        with st.container():
            st.title("Ballchasing Data Ingestion", text_alignment = "center")
            st.space(size = "large")

            with st.form(key="player_info_form", clear_on_submit=True):
                player_name: int = st.text_input(label = "**ENTER PLAYER NAME**", value="", placeholder = "John Doe", max_chars = 32, width = 200)
                game_count: int = st.number_input(label = "**ENTER NUMBER OF GAMES**", value=None, placeholder = "(Between 1 and 200)", min_value = 1, max_value = 200, width = 200)

                submit_button = st.form_submit_button(label="Submit")

            if submit_button:
                if not player_name.isalnum():
                    st.error(f"'{player_name}' must be comprised of alpha-numeric characters.")
                elif game_count is None:
                    st.error("Game count must not be null.")
                else:
                    if player_name in st.session_state["df_manifest"]:
                        overwrite_popup(player_name, game_count)
                    else:
                        st.success(f"Form submitted successfully. Pulling {player_name}'s Ballchasing data from the last {game_count} games!")
                        add_df_to_list(player_name, game_count)                
    else:
        st.title("Please add a Ballchasing API Authentication Key to use this Scouting Tool. Visit https://ballchasing.com/upload to find your key.")

                