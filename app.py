import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Sample Page Basketball Box Score",
    page_icon="🏀",
    layout="wide"
)

# --- CUSTOM CSS FOR A PRO LOOK ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    [data-testid="stHeader"] {
        background-color: #111111;
    }
    h1, h2, h3 {
        font-family: 'Arial Black', Gadget, sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA CONNECTION ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    sheet_url = os.environ.get("GSHEETS_SPREADSHEET_URL")
    
    if not sheet_url:
        st.error("Error: GSHEETS_SPREADSHEET_URL environment variable is missing.")
    else:
        df = conn.read(spreadsheet=sheet_url)

        # --- SIDEBAR FILTERS ---
        st.sidebar.header("Navigation")
        if 'Team' in df.columns:
            teams = df['Team'].unique().tolist()
            selected_team = st.sidebar.selectbox("Select Team", options=teams)
            filtered_df = df[df['Team'] == selected_team]

            # --- HEADER SECTION (ESPN STYLE) ---
            col_logo, col_text = st.columns([1, 4])
            with col_logo:
                # Replace this URL with your actual Team Logo or Mascot
                st.image("https://cdn-icons-png.flaticon.com/512/889/889500.png", width=100)
            with col_text:
                st.title(f"{selected_team} | Game Center")
                st.write("2026 Season • Regular Game Statistics")

            # --- TOP PERFORMERS (METRIC CARDS) ---
            st.divider()
            m1, m2, m3, m4 = st.columns(4)
            if not filtered_df.empty:
                top_pts = filtered_df.loc[filtered_df['PTS'].idxmax()]
                top_reb = filtered_df.loc[filtered_df['REB_TOT'].idxmax()]
                top_ast = filtered_df.loc[filtered_df['AST'].idxmax()]
                total_team_pts = filtered_df['PTS'].sum()

                m1.metric("TEAM TOTAL", f"{total_team_pts} PTS", delta="Final Score")
                m2.metric("TOP SCORER", top_pts['Name'], f"{top_pts['PTS']} PTS")
                m3.metric("REBOUND LEADER", top_reb['Name'], f"{top_reb['REB_TOT']} REB")
                m4.metric("PLAYMAKER", top_ast['Name'], f"{top_ast['AST']} AST")

            # --- INTERACTIVE TABS ---
            tab_box, tab_charts, tab_photos = st.tabs(["📊 BOX SCORE", "📈 ANALYTICS", "📸 GAME PHOTOS"])

            with tab_box:
                st.subheader("Individual Player Stats")
                # Configure columns to look professional
                st.dataframe(
                    filtered_df[['Name', 'No', 'Min', 'PTS', 'REB_TOT', 'AST', 'STL', 'BLK', 'TO', 'Plus/Minus']],
                    column_config={
                        "Name": st.column_config.TextColumn("PLAYER", width="medium"),
                        "PTS": st.column_config.NumberColumn("PTS", format="%d 🔥"),
                        "Plus/Minus": st.column_config.NumberColumn("+/-", format="%+d"),
                        "REB_TOT": "REB",
                    },
                    hide_index=True,
                    use_container_width=True
                )

            with tab_charts:
                st.subheader("Scoring Distribution")
                st.bar_chart(filtered_df, x="Name", y="PTS", color="#ff4b4b")
                
                st.subheader("Rebounds vs Assists")
                st.scatter_chart(filtered_df, x="REB_TOT", y="AST", color="Name")

            with tab_photos:
                st.subheader("Game Gallery")
                # Example: Use a 3-column grid for photos
                p_col1, p_col2, p_col3 = st.columns(3)
                with p_col1:
                    st.image("https://via.placeholder.com/400x300?text=Game+Highlight+1", caption="Fast Break")
                with p_col2:
                    st.image("https://via.placeholder.com/400x300?text=Game+Highlight+2", caption="Defense Wall")
                with p_col3:
                    st.image("https://via.placeholder.com/400x300?text=Game+Highlight+3", caption="Three Pointer")

        else:
            st.warning("Could not find 'Team' column. Please check your Google Sheet data.")

except Exception as e:
    st.error(f"Failed to load dashboard: {e}")
