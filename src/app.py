import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the CSV data from the provided link
url = "https://media.githubusercontent.com/media/sunshineluyao/icp-nns-db/main/data/proposals_no_empty.csv"
df = pd.read_csv(url)

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Prepare data for the treemap
topic_counts = df['topic'].value_counts().reset_index()
topic_counts.columns = ['Topic', 'Count']

# Create a treemap using Plotly Express
fig = px.treemap(topic_counts, path=['Topic'], values='Count', title='Distribution of Topics')
fig.update_traces(marker=dict(colors=['pink']))  # Set the color to pink

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Internet Computer Protocol NNS Governance System Dashboard: Topic"),
    
    html.P([
        "Choose the proposal status to view the distributions of proposal topics. ",
        html.I("Notes: Topic is the main subject of the proposal; Status is the current standing of the proposal, be it pending, accepted, negated, or unsuccessful.")
    ]),

    dcc.Dropdown(
        id='status-dropdown',
        options=[{'label': status, 'value': status} for status in df['status'].unique()],
        value=df['status'].unique()[0],
        multi=False
    ),

    dcc.Graph(id='bar-plot', figure=fig)  # Set the initial figure to the treemap
])

# Create a callback to update the treemap based on the selected status
@app.callback(
    Output('bar-plot', 'figure'),
    Input('status-dropdown', 'value')
)
def update_bar_plot(selected_status):
    filtered_df = df[df['status'] == selected_status]
    topic_counts_filtered = filtered_df['topic'].value_counts().reset_index()
    topic_counts_filtered.columns = ['Topic', 'Count']

    fig = px.treemap(topic_counts_filtered, path=['Topic'], values='Count', title=f'Distribution of Topics for {selected_status} Proposals')
    fig.update_traces(marker=dict(colors=['pink']))  # Set the color to pink
    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
