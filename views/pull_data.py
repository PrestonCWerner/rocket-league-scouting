import streamlit as st
import pandas as pd
from utils.player_replay_ingestion import ingest_data


if __name__ == "__main__":
    st.set_page_config(layout = "centered")
    with st.sidebar:
        if st.button("Clear Cache"):
            st.cache_data.clear()
    with st.container():
        st.title("Ballchasing Data Ingestion", text_alignment = "center")
        st.space(size = "large")

        with st.form(key="player_info_form", clear_on_submit=True):
            player_name: int = st.text_input(label = "**ENTER PLAYER NAME**", value="", placeholder = "John Doe", max_chars = 32, width = 200)
            game_count: int = st.number_input(label = "**ENTER NUMBER OF GAMES**", value=None, placeholder = "(Between 1 and 50)", min_value = 1, max_value = 50, width = 200)

            submit_button = st.form_submit_button(label="Submit")

        name_validation_list: list = [" ", "/", "\\", "<", ">", "\"", "\'"]
        char_flag = False
        df_exists = False

        if submit_button:
            for char in player_name:
                if char in name_validation_list:
                    st.error(f"Character '{char}' is not a valid character in '{player_name}'.")
                    char_flag = True
                    break
            
            if game_count is None:
                st.error("Game count must not be null.")
                
            
            if player_name + "_" + str(game_count) in st.session_state["df_manifest"]:
                st.error(f"DataFrame already exists for player {player_name}'s last {game_count} games.")
                df_exists = True
            
            if not char_flag and game_count is not None and not df_exists:
                st.success(f"Form submitted successfully. Pulling {player_name}'s Ballchasing data from the last {game_count} games!")
                with st.spinner("Loading data..."):
                    new_df: pd.DataFrame = ingest_data(player_name, game_count, st.session_state["api_key"])
                    st.session_state["df_manifest"].append(f"{player_name}_{game_count}")
                    st.session_state["df_dict"][f"{player_name}_{game_count}"] = new_df
                
                st.success(f"Successfully loaded data into DataFrame list.")

                