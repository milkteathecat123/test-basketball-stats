import dash
from dash import dcc, html, dash_table, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import os

# 1. Initialize the App with a Dark Sports Theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])
server = app.server  # Required for Render deployment

# 2. Layout: Designing the "Game Center"
app.layout = dbc.Container([
    # Header Section
    dbc.Row([
        dbc.Col(html.H1("🏀 BASKETBALL STATS CENTER", className="text-center my-4 text-warning"), width=12)
    ]),

    # Team Selector Dropdown
    dbc.Row([
        dbc.Col([
            html.Label("Choose Team:", className="fw-bold"),
            dcc.Dropdown(id='team-selector', className="text-dark mb-4")
        ], width=4)
    ], justify="center"),

    # Top Performer Metric Cards
    dbc.Row([
        dbc.Col(dbc.Card(id='pts-card', body=True, color="primary", inverse=True), width=4),
        dbc.Col(dbc.Card(id='reb-card', body=True, color="success", inverse=True), width=4),
        dbc.Col(dbc.Card(id='ast-card', body=True, color="info", inverse=True), width=4),
    ], className="mb-4 text-center"),

    # Box Score Table
    dbc.Row([
        dbc.Col([
            html.H3("Interactive Box Score", className="mb-3"),
            html.Div(id='table-container')
        ], width=12)
    ])
], fluid=True)

# 3. Callbacks: The Interactive Logic
@app.callback(
    [Output('team-selector', 'options'),
     Output('team-selector', 'value')],
    [Input('team-selector', 'id')] # Trigger on page load
)
def populate_teams(_):
    # Fetch data from your Google Sheet URL
    url = os.environ.get("GSHEETS_SPREADSHEET_URL")
    # Using export to CSV for simple public sheet reading
    csv_url = url.replace('/edit?usp=sharing', '/export?format=csv')
    df = pd.read_csv(csv_url)
    
    teams = sorted(df['Team'].unique())
    return [{'label': t, 'value': t} for t in teams], teams[0]

@app.callback(
    [Output('pts-card', 'children'),
     Output('reb-card', 'children'),
     Output('ast-card', 'children'),
     Output('table-container', 'children')],
    [Input('team-selector', 'value')]
)
def update_stats(selected_team):
    url = os.environ.get("GSHEETS_SPREADSHEET_URL")
    csv_url = url.replace('/edit?usp=sharing', '/export?format=csv')
    df = pd.read_csv(csv_url)
    
    filtered = df[df['Team'] == selected_team]
    
    # Identify Leaders
    top_pts = filtered.loc[filtered['PTS'].idxmax()]
    top_reb = filtered.loc[filtered['REB_TOT'].idxmax()]
    top_ast = filtered.loc[filtered['AST'].idxmax()]

    # Create Metric Card Content
    pts_content = [html.H5("PTS LEADER"), html.H3(top_pts['Name']), html.P(f"{top_pts['PTS']} Points")]
    reb_content = [html.H5("REB LEADER"), html.H3(top_reb['Name']), html.P(f"{top_reb['REB_TOT']} Rebounds")]
    ast_content = [html.H5("AST LEADER"), html.H3(top_ast['Name']), html.P(f"{top_ast['AST']} Assists")]

    # Create the Box Score Table
    table = dash_table.DataTable(
        data=filtered.to_dict('records'),
        columns=[{"name": i, "id": i} for i in ['Name', 'No', 'Min', 'PTS', 'REB_TOT', 'AST', 'STL', 'BLK', 'Plus/Minus']],
        style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white', 'fontWeight': 'bold'},
        style_cell={'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white', 'textAlign': 'left'},
        sort_action="native",
        filter_action="native",
        page_size=15
    )

    return pts_content, reb_content, ast_content, table

if __name__ == "__main__":
    app.run_server(debug=True)
