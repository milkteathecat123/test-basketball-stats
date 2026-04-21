import dash
from dash import dcc, html, dash_table, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import os

# 1. Initialize the App with a Professional Theme
# 'SUPERHERO' is great for a dark sports vibe; 'FLATLY' for a clean ESPN look.
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])
server = app.server # Needed for Render

# 2. Data Loading (Simulated for setup)
# Replace this with your actual gspread logic from earlier
def get_data():
    url = os.environ.get("GSHEETS_SPREADSHEET_URL")
    # For now, we'll assume df is loaded here
    return pd.read_csv("your_temp_data.csv") 

# 3. App Layout (The "Professional" Box Score Structure)
app.layout = dbc.Container([
    # Header Row
    dbc.Row([
        dbc.Col(html.H1("🏀 PRO STATS CENTER", className="text-center my-4"), width=12)
    ]),

    # Team Selector
    dbc.Row([
        dbc.Col([
            html.Label("Select Team:"),
            dcc.Dropdown(id='team-dropdown', options=[], value=None, className="mb-4")
        ], width=4)
    ]),

    # Metric Cards (ESPN Style)
    dbc.Row([
        dbc.Col(dbc.Card(id='pts-leader-card', color="primary", inverse=True), width=4),
        dbc.Col(dbc.Card(id='reb-leader-card', color="success", inverse=True), width=4),
        dbc.Col(dbc.Card(id='ast-leader-card', color="info", inverse=True), width=4),
    ], className="mb-4"),

    # Main Box Score Table
    dbc.Row([
        dbc.Col([
            html.Div(id='box-score-container')
        ], width=12)
    ])
], fluid=True)

# 4. Callbacks (The "Interactive" Logic)
@app.callback(
    [Output('pts-leader-card', 'children'),
     Output('box-score-container', 'children')],
    [Input('team-dropdown', 'value')]
)
def update_dashboard(selected_team):
    # This logic only runs when the dropdown changes
    # You would filter your dataframe here and return the updated components
    return "Leader Name", "Table HTML here"

if __name__ == "__main__":
    app.run_server(debug=True)
