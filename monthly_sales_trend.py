# Import necessary libraries
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the dataset
data = pd.read_excel("C:/Users/Chandru/OneDrive/Desktop/Python Visuals/Sample - Superstore.xls", sheet_name="Orders")

# Extract year and month from the 'Order Date' column
data['Year'] = data['Order Date'].dt.year
data['Month'] = data['Order Date'].dt.month_name()

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1("Sales Trends"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': year, 'value': year} for year in data['Year'].unique()],
        value=data['Year'].unique(),
        multi=True
    ),
    dcc.Dropdown(
        id='month-dropdown',
        options=[{'label': month, 'value': month} for month in data['Month'].unique()],
        value=data['Month'].unique(),
        multi=True
    ),
    dcc.Graph(id='line-chart')
])

# Define callback to update graph
@app.callback(
    Output('line-chart', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_graph(selected_years, selected_months):
    filtered_data = data[data['Year'].isin(selected_years) & data['Month'].isin(selected_months)]
    fig = px.line(filtered_data.groupby(['Year', 'Month'])['Sales'].sum().reset_index(), x='Month', y='Sales', color='Year', title='Monthly Sales Trends')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
