# All imports that you would need are already provided.
import pandas as pd
import plotly.express as px

from bson import ObjectId
from pymongo import MongoClient
from dash import Dash, html, callback, Output, Input, dash_table, dcc

# Please do not modify the database name
DATABASE_NAME = "dash-exam"
# Insert your MongoDB connection string here
CONNECTION_STRING = "mongodb+srv://ilievayana:iylfRpWikjic485Y@cluster0.ij9wh5k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

app = Dash(__name__)
# Replace None with the layout of the application based on the instructions
app.layout = html.Div(id= "html-div", children=[
    html.H2(children="Temp sensors"),
    dash_table.DataTable(id="sensor-table"),
    html.Br(),
    dcc.Graph(id='graph'),
    html.Label("Select:"),
    dcc.RadioItems(
        id='radio',
        options=[],
        value=''
    ),
    dcc.Interval(id="interval", interval=1000, n_intervals=0)
])

# Write the callback function(s) based on the instructions
@callback(
    Output("sensor-table", "data"),
    Input("interval", "n_intervals")
)
def update_sensor_table(_):
    sensors = list(thermometer_collection.find({}))
    for sensor in sensors:
        sensor["_id"] = str(sensor["_id"])
    return sensors

@callback(
    Output('graph', 'figure'),
    [Input('interval', 'n_intervals'), Input('radio', 'value')]
)
def show_graph(_,selected_id):
    if selected_id == 'All' or not selected_id:
        temperatures = list(temperature_collection.find({}))
    else:
        temperatures = list(temperature_collection.find({'thermometer_id': ObjectId(selected_id)}))
        
    # temperatures = list(temperature_collection.find({}))
    df = pd.DataFrame(temperatures)
    df['timestamp'] = pd.to_datetime(df['timestamp']) 
    
    fig = px.line(df, x='timestamp', y='value', color='thermometer_id')
    fig.update_layout(title='Temperature Graph',
                      xaxis_title='Timestamp',
                      yaxis_title='Temperature')
    return fig
    
@callback(
    Output("radio", "options"),
    Input("interval", "n_intervals")
)
def update_options(_):
    them_ids = temperature_collection.distinct("thermometer_id")
    options = [{"label": "All", "value": "All"}]  
    options += [{"label": str(them_id), "value": str(them_id)} for them_id in them_ids]
    return options


# Please do not modify the below function
# Use the thermometer_collection and temperature_collection objects to query the database
if __name__ == "__main__":
    mongo_client = MongoClient(CONNECTION_STRING)
    database = mongo_client.get_database(DATABASE_NAME)
    thermometer_collection = database.get_collection("thermometers")
    temperature_collection = database.get_collection("temperatures")
    app.run(debug=True, port=8050)