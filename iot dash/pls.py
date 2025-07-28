from pymongo import MongoClient
from dash import Dash, dcc, html, Input, Output, callback, dash_table

URI = "mongodb+srv://test:test@iotexercisecluster.8archtp.mongodb.net/?retryWrites=true&w=majority&appName=IoTExerciseCluster"

app = Dash(__name__)
app.layout = html.Div([
    html.H4("Live temperature feed"),
    html.P("Some text"),
    dash_table.DataTable(id="sensor-update-table", page_size=100),
    dcc.Interval(id="interval-component", interval=1000, n_intervals=0)
])


@callback(Output("sensor-update-table", "data"),
          Input("interval-component", "n_intervals"))
def update_sensor_table(n_intervals):
    sensors = list(sensor_collection.find({}))
    for sensor in sensors:
        sensor["_id"] = str(sensor["_id"])
    return sensors


if __name__ == "__main__":
    # Setup mongo client
    client = MongoClient(URI)
    database = client.get_database("mongo_exam_database")
    sensor_collection = database.get_collection("air_quality_sensors")
    sensor_data_collection = database.get_collection("air_quality_sensor_data")

    # Start the Dash app
    app.run(debug=True, port=8050)