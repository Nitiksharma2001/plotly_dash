import dash, os
from dash import Dash, html, dcc, Output, Input, callback
import plotly.express as px
from dotenv import load_dotenv
from connection import Connection

load_dotenv() 
app = Dash()

# Set these as environment variables in Dash Enterprise or locally
SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME')
HTTP_PATH = os.getenv('HTTP_PATH')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

connection = Connection(SERVER_HOSTNAME, HTTP_PATH, ACCESS_TOKEN)

# Configure according to your table name in Databricks
DB_NAME = "default"
TABLE_NAME = "academic_performance_dataset"

global_options = []
app.layout = html.Div(
    [
        html.Div(
          id='my-dropdown-parent',
          children=[
              dcc.Dropdown(
                  id='my-dropdown',
                  options=[]
              ),
        ], style={"margin-bottom": "10px"},),
        dcc.Input(id="val-selector-2", type="number", min=2010, max=2015, value=2010),
        dcc.Loading(dcc.Graph(id="sample-chart-2")),
    ],
)

@app.callback(Output('my-dropdown', 'options'),
              Input('my-dropdown-parent', 'n_clicks'))
def change_my_dropdown_options(n_clicks):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    
    query = f"SELECT DISTINCT(`Prog Code`) from {DB_NAME}.{TABLE_NAME} LIMIT 5 OFFSET {5*n_clicks}"

    df = connection.make_query(query)
    fetch_options = df.to_pandas()['Prog Code'].to_list()

    global_options.extend([{'label': value, 'value': value} for value in fetch_options])

    return global_options

@callback(Output("sample-chart-2", "figure"), Input("val-selector-2", "value"))
def create_chart(selected_val):
    query = f"SELECT * FROM {DB_NAME}.{TABLE_NAME} WHERE YoG = {selected_val}"

    df = connection.make_query(query)
    df = df.to_pandas()

    return px.scatter(df, x="CGPA", y="CGPA200")

if __name__ == "__main__":
    app.run(debug=True)