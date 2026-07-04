import streamlit as st
import pandas as pd
from utils.player_replay_ingestion import ingest_data

@st.dialog("Ballchasing API Auth Key Submission", dismissible = False)
def set_api_auth_key() -> None:
    with st.form(key="api_key_submission", clear_on_submit=True):
        api_auth_key: str = st.text_input(label = "**ENTER AUTH KEY**", value=None, placeholder = "ABCDEFGHI12345678", type = "password", max_chars = 40, width = 200)
        submit_button = st.form_submit_button(label="Submit")

        if submit_button:
            if api_auth_key is None:
                st.error("Please put an API Auth Key in the text input.")
            elif not api_auth_key.isalnum():
                st.error("API Auth Key is not a valid key. Please double-check your Ballchasing API key.")
            elif len(api_auth_key) < 40:
                st.error(f"API Auth Key is not a valid key. Auth Key was of length {len(api_auth_key)} characters, but expected 40 characters. Please double-check your Ballchasing API key.")
            else:
                st.session_state["api_key"] = api_auth_key
                st.success("API Authorization Key added to this session. You may close this window.")
                st.rerun()

if __name__ == "__main__":
    st.set_page_config(layout = "centered")
    with st.sidebar:
        if st.button("Clear Cache"):
            st.cache_data.clear()
        
        if st.button("Change API Authentication Key"):
            set_api_auth_key()

    with st.container():
        st.title("Ballchasing Data Ingestion", text_alignment = "center")
        st.space(size = "large")

        with st.form(key="player_info_form", clear_on_submit=True):
            player_name: int = st.text_input(label = "**ENTER PLAYER NAME**", value="", placeholder = "John Doe", max_chars = 32, width = 200)
            game_count: int = st.number_input(label = "**ENTER NUMBER OF GAMES**", value=None, placeholder = "(Between 1 and 50)", min_value = 1, max_value = 50, width = 200)

            submit_button = st.form_submit_button(label="Submit")

        if submit_button:
            
            if not player_name.isalnum():
                st.error(f"'{player_name}' must be comprised of alpha-numeric characters.")
            elif game_count is None:
                st.error("Game count must not be null.")
            elif player_name + "_" + str(game_count) in st.session_state["df_manifest"]:
                st.error(f"DataFrame already exists for player {player_name}'s last {game_count} games.")
                df_exists = True         
            else:
                st.success(f"Form submitted successfully. Pulling {player_name}'s Ballchasing data from the last {game_count} games!")
                with st.spinner("Loading data..."):
                    new_df: pd.DataFrame = ingest_data(player_name, game_count, st.session_state["api_key"])
                    st.session_state["df_manifest"].append(f"{player_name}_{game_count}")
                    st.session_state["df_dict"][f"{player_name}_{game_count}"] = new_df
                
                st.success(f"Successfully loaded data into DataFrame list.")

                