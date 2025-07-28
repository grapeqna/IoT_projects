from pymongo import MongoClient
from dash import Dash, html, callback, Output, Input, dash_table, dcc
import plotly.express as px
import pandas as pd

DATABASE_NAME = "mongo_exam_database"
CONNECTION_STRING = "mongodb+srv://ilievayana:iylfRpWikjic485Y@cluster0.ij9wh5k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Same initialization as for a Flask app, but for a Dash app
app = Dash(__name__)
# The layout is the most important part of a Dash app
# It defines the structure of the app

# The layout is a tree of components, surrounded by an HTML DIV element
# We can insert any components we want inside the DIV element, including:
# - HTML elements (like headers, paragraphs, images, etc.)
# - Dash components (like tables, graphs, etc.)

# Every element in the layout is a component, and every component has properties
# The properties of a component can be set when creating the component
# Or they can be updated using callbacks
# Most important is the ID property, which is used to identify the component in the callbacks

# In this case, we have two tables that will be updated every second
# The first table will show the air quality sensors
# The second table will show the data collected by the sensors
app.layout = html.Div(id="html-div", children=[
    html.H2(children="Air quality sensor table"),
    dash_table.DataTable(id="sensor-table"),
    html.Br(),
    html.Br(),
    html.Br(),
    dash_table.DataTable(id="sensor-data-table"),
    html.Br(),
    dcc.Graph(id='graph'),
    html.Label("Select City:"),
    dcc.RadioItems(
        id='radio',
        options=[],
        value=''
    ),
    # Interval component to trigger the callbacks every second
    # It is hidden in the layout, so it is not visible to the user
    # It contains ID, interval (in milliseconds), and n_intervals (number of times the interval has passed)
    # When the interval triggers, it increments n_intervals by 1 and calls the callbacks
    dcc.Interval(id="interval", interval=1000, n_intervals=0)
])


# Callbacks are used to update the components in the layout
# They are defined with the @callback decorator
# The decorator takes the Output and Input components as arguments
# The Output component is the component that will be updated, found by its ID
# The Input component is the component that triggers the update, found by its ID
# The function that follows the decorator is the callback function
# It takes the trigger as an argument (_ if we don't use it)
# The callback function returns the new value of the Output component and updates it in the layout
# In this case, the tables are updated with the data from the MongoDB collections in the form of lists of dictionaries

# If we don't have the interval component, we have to use the main DIV component as the trigger.
# This way when the page is loaded, the callback is triggered and the tables are updated.
# @callback(
#     Output("sensor-table", "data"),
#     Input("html-div", "children")
# )
@callback(
    Output("sensor-table", "data"),
    Input("interval", "n_intervals")
)
def update_sensor_table(_):
    sensors = list(air_quality_sensor_collection.find({}))
    for sensor in sensors:
        sensor["_id"] = str(sensor["_id"])
    return sensors


@callback(
    Output("sensor-data-table", "data"),
    Input("interval", "n_intervals")
)
def update_sensor_data_table(_):
    sensor_data = list(air_quality_sensor_data_collection.find({}))
    for data in sensor_data:
        data["_id"] = str(data["_id"])
        data["air_quality_sensor_id"] = str(data["air_quality_sensor_id"])
    return sensor_data

@callback(
    Output('graph', 'figure'),
    [Input('interval', 'n_intervals'), Input('radio', 'value')]
)
def show_graph(_, selected_city):
    if not selected_city:
        df= air_quality_sensor_data_collection.find({})
        fig= px.line(df,x='timestamp', y='value', title=f'Air Quality Data for {selected_city}' )
        return fig
    
    sensor_data = []
    for document in list(air_quality_sensor_data_collection.find({})):
        sensor_id = document.get('air_quality_sensor_id')
        if sensor_id:
            # Find corresponding sensor document in collection2
            sensor_document = air_quality_sensor_collection.find_one({'_id': sensor_id})
            if sensor_document and sensor_document.get('city') == selected_city:
                sensor_data.append(document)

    if not sensor_data:
        return {}

    df = pd.DataFrame(sensor_data)
    fig = px.line(df, x='timestamp', y='value', title=f'Air Quality Data for {selected_city}')
    return fig

@callback(
    Output("radio", "options"),
    Input("interval", "n_intervals")
)
def update_city_options(_):
    cities = air_quality_sensor_collection.distinct("city")
    return [{"label": city, "value": city} for city in cities]

if __name__ == "__main__":
    mongo_client = MongoClient(CONNECTION_STRING)
    database = mongo_client.get_database(DATABASE_NAME)
    air_quality_sensor_collection = database.get_collection("air_quality_sensors")
    air_quality_sensor_data_collection = database.get_collection("air_quality_sensor_data")
    app.run(debug=True, port=8050)
