# Rocket League Scouting Tool Project

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Screenshots](#screenshots)
- [Instructions](#instructions)
- [Roadmap](#roadmap)

## OVERVIEW
An end-to-end data engineering project that ingests Rocket League match data from the Ballchasing API, transforms it into analytics-ready datasets using Python and DuckDB, and serves interactive scouting dashboards through Streamlit.

Current Status: Active development. Core ingestion, transformation, and analytics functionality are complete. Current work focuses on performance improvements, additional visualizations, and production-readiness.

## ARCHITECTURE
Ballchasing API &rarr; Python Data Ingestion &rarr; Raw Match Data &rarr; Locally-Saved CSV  &rarr; Pandas Data Cleaning &rarr; DuckDB Transformations &rarr; Analytics-Ready Tables &rarr; Streamlit Dashboard &rarr; Player Performance Analysis

## SCREENSHOTS

### Data Ingestion
<img width="2398" height="985" alt="csv_file_saved" src="https://github.com/user-attachments/assets/06775ae2-faff-4a58-a231-aeab5ab7485f" />

### Player Analysis - Core Statistics
<img width="2489" height="1112" alt="player_analysis_core" src="https://github.com/user-attachments/assets/e8ae1ff7-27ba-4a2d-a609-a9199cae5125" />

### Player Analysis - Movement Statistics
<img width="2516" height="916" alt="player_analysis_movement" src="https://github.com/user-attachments/assets/d78691ab-2af9-43a9-b96f-a64a24a8dbf1" />

### Player Analysis - Boost Statistics
<img width="2431" height="1103" alt="player_analysis_boost" src="https://github.com/user-attachments/assets/5760a655-9d92-43c4-b7cb-3aa2cedbd0a7" />

### Player Analysis - File Picker
<img width="303" height="471" alt="file_selection" src="https://github.com/user-attachments/assets/1fe5db61-d35f-4574-9016-546c45e16298" />


### Player Analysis - Replay Data Not Found
<img width="2429" height="1149" alt="replays_not_found_filter" src="https://github.com/user-attachments/assets/a0edb360-0624-41fe-b223-d1988774e2ad" />



## INSTRUCTIONS

### STEP 1: Creating the proper environment.
1. Ensure that you have Python installed in your local environment. If you don't have it, you can download it from https://www.python.org/downloads/.
2. Ensure that you have Pip installed in your local environment. If you do not have pip, you can try running the following script in your preferred terminal. 
```
    python -m ensurepip --default-pip
```
3. With Python and pip installed, you will now need to install the required dependencies to run the Streamlit app. This may be accomplished with the following script (Make sure you are in the root folder of the project):
```
    pip install -r requirements.txt
```
4. Create a .env file in the root folder of the project. Copy and paste the following block into your .env file (replacing PLACEHOLDER with your personal API authorization key for Ballchasing.):
```
    API_AUTHORIZATION_KEY=PLACEHOLDER
    BASE_URL=https://ballchasing.com/api/replays
```
5. Create a .logs folder in the root directory with one file: 'player_replay_ingestion.logs'

### STEP 2: Run the app
1. Once your environment is setup, you can run the app by executing the following script from the root directory of the project:
```
    streamlit run app.py
```
2. You are now able to access the full functionality of the project: creating datasets from Ballchasing data pulled based on Player Name and the N last games played!

### STEP 3: ???


### STEP 4: Profit
You may now analyze player performances much easier than before and maintain historical records of player performances across time. Woo-hoo!

## ROADMAP
1. Add functionality to upload a CSV or similar with player names and game counts to ingest a large amount of data at once.
2. Add further options for filtering by playlist type (private, public) and rank for competitive games (see how players perform in their Champ lobbies vs Diamond lobbies, and so on).
3. Reformat analytics reports to be more eye-friendly.
4. Containerize application with Docker.
