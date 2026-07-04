import streamlit as st

home_page = st.Page("views/pull_data.py", title="Home - Ingest Data", icon="🏠", default=True)
analytics_page = st.Page("views/player_analysis.py", title="Player Analysis", icon="📊")

# Initialize navigation
pg = st.navigation([home_page, analytics_page])

# Run the selected page
pg.run()