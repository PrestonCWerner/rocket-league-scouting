import streamlit as st

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