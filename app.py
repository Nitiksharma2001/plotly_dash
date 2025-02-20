import dash
import os
from dash import Dash, html, dcc, Output, Input, callback
from databricks import sql
import plotly.express as px

from dotenv import load_dotenv

load_dotenv() 

app = Dash()
server = app.server

# Set these as environment variables in Dash Enterprise or locally
SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME')
HTTP_PATH = os.getenv('HTTP_PATH')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

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
    
    connection = sql.connect(
        server_hostname=SERVER_HOSTNAME, http_path=HTTP_PATH, access_token=ACCESS_TOKEN
    )
    cursor = connection.cursor()
    query = f"SELECT DISTINCT(`Prog Code`) from {DB_NAME}.{TABLE_NAME} LIMIT 5 OFFSET {5*n_clicks}"
    cursor.execute(query)
    df = cursor.fetchall_arrow()

    lst = df.to_pandas()['Prog Code'].to_list()

    cursor.close()
    connection.close()

    global_options.extend([{'label': value, 'value': value} for value in lst])

    return global_options

@callback(Output("sample-chart-2", "figure"), Input("val-selector-2", "value"))
def create_chart(selected_val):
    connection = sql.connect(
        server_hostname=SERVER_HOSTNAME, http_path=HTTP_PATH, access_token=ACCESS_TOKEN
    )
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {DB_NAME}.{TABLE_NAME} WHERE YoG = {selected_val}")
    df = cursor.fetchall_arrow()
    df = df.to_pandas()

    cursor.close()
    connection.close()

    return px.scatter(df, x="CGPA", y="CGPA200")

if __name__ == "__main__":
    app.run(debug=True)
