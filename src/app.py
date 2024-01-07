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

# Create a bar plot using Plotly Express with a log-scale y-axis
# Replace 'action' with 'topic' in the plot creation
fig = px.bar(df['topic'].value_counts(), x=df['topic'].value_counts().index, y=df['topic'].value_counts().values, labels={'x': 'Topic', 'y': 'Count'}, title='Distribution of Topics')
fig.update_yaxes(type="log")  # Set y-axis to logarithmic scale

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

    dcc.Graph(id='bar-plot')
])

# Create a callback to update the bar plot based on the selected status
@app.callback(
    Output('bar-plot', 'figure'),
    Input('status-dropdown', 'value')
)
def update_bar_plot(selected_status):
    # Update here as well to use 'topic' instead of 'action'
    filtered_df = df[df['status'] == selected_status]
    fig = px.bar(filtered_df['topic'].value_counts(), x=filtered_df['topic'].value_counts().index,
                 y=filtered_df['topic'].value_counts().values, labels={'x': 'Topic', 'y': 'Count'},
                 title=f'Distribution of Topics for {selected_status} Proposals')
    fig.update_yaxes(type="log")  # Set y-axis to logarithmic scale
    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
