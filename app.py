import streamlit as st
import requests

@st.dialog("Ballchasing API Auth Key Submission", dismissible = False)
def set_api_auth_key() -> None:
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
    
                


home_page = st.Page("views/pull_data.py", title="Home - Ingest Data", icon="🏠", default=True)
analytics_page = st.Page("views/player_analysis.py", title="Player Analysis", icon="📊")

# Initialize navigation
pg = st.navigation([home_page, analytics_page])

if "df_manifest" not in st.session_state:
    # Initialize session_state dataframe manifest 
    st.session_state["df_manifest"] = []

if "df_dict" not in st.session_state:
    st.session_state["df_dict"] = {}    

if "api_key" not in st.session_state:
    set_api_auth_key()

# Run the selected page
pg.run()