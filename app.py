import streamlit as st

home_page = st.Page("views/pull_data.py", title="Home - Ingest Data", icon="🏠", default=True)
analytics_page = st.Page("views/player_analysis.py", title="Player Analysis", icon="📊")

# Initialize navigation
pg = st.navigation([home_page, analytics_page])

if "df_manifest" not in st.session_state:
    # Initialize session_state dataframe manifest 
    st.session_state["df_manifest"] = []

if "df_dict" not in st.session_state:
    st.session_state["df_dict"] = {}    

# Run the selected page
pg.run()