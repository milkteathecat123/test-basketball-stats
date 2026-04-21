import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import os

# Page setup
st.set_page_config(page_title="Basketball Stats Tracker", layout="wide")

st.title("🏀 Season Stats Dashboard")

# 1. Connect to your Google Sheet using the Render Environment Variable
# This uses the GSHEETS_SPREADSHEET_URL key you created in Render settings
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    sheet_url = os.environ.get("GSHEETS_SPREADSHEET_URL")
    
    if not sheet_url:
        st.error("Error: GSHEETS_SPREADSHEET_URL not found in Render Environment Variables.")
    else:
        # Read the data from the Google Sheet
        df = conn.read(spreadsheet=sheet_url)

        # 2. Sidebar Filters
        st.sidebar.header("Filter Stats")
        
        # Ensure the 'Team' column exists before filtering
        if 'Team' in df.columns:
            teams = df['Team'].unique().tolist()
            selected_team = st.sidebar.selectbox("Select Team", options=teams)

            # Filter data based on selection
            filtered_df = df[df['Team'] == selected_team]

            # 3. Top Performers (Metric Cards)
            st.subheader(f"Top Performers: {selected_team}")
            col1, col2, col3 = st.columns(3)

            if not filtered_df.empty:
                # Finding leaders based on your sheet columns
                top_scorer = filtered_df.loc[filtered_df['PTS'].idxmax()]
                top_rebounder = filtered_df.loc[filtered_df['REB_TOT'].idxmax()]
                top_playmaker = filtered_df.loc[filtered_df['AST'].idxmax()]

                col1.metric("Points Leader", top_scorer['Name'], f"{top_scorer['PTS']} PTS")
                col2.metric("Rebound Leader", top_rebounder['Name'], f"{top_rebounder['REB_TOT']} REB")
                col3.metric("Assist Leader", top_playmaker['Name'], f"{top_playmaker['AST']} AST")

            # 4. Interactive Leaderboard
            st.divider()
            st.subheader("Full Player Statistics")
            # Displays the spreadsheet data in an interactive table
            st.dataframe(filtered_df.sort_values(by="PTS", ascending=False), use_container_width=True)

            # 5. Visual Chart
            st.subheader("Scoring Distribution")
            st.bar_chart(data=filtered_df, x="Name", y="PTS")
        else:
            st.warning("The 'Team' column was not found in your Google Sheet. Please check Column A.")

except Exception as e:
    st.error(f"An error occurred while connecting to the data: {e}")
