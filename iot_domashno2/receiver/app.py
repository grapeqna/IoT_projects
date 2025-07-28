from flask import Flask, request, Response
from pysondb import db
import matplotlib.pyplot as plt
import io

a = db.getDb("static/db.json")

app = Flask(__name__)
app.json.sort_keys = False

def calc_stats(id):
    data = a.getByQuery({"device_id": str(id)})
    if len(data) <= 0:
        return (id, 0, 0, 0)
    min_val = 0xFFFFFFFF
    max_val = 0
    sum_val = 0
    for entry in data:
        val = entry['value']
        if val < min_val:
            min_val = val
        if val > max_val:
            max_val = val
        sum_val += val    
        avg_val = sum_val / len(data)
    return (id, min_val, max_val, avg_val)

@app.route('/stats', methods=['GET'])
def getStats():
    i = 1
    res = []
    while len(a.getByQuery({"device_id": str(i)})) > 0:
        res.append(calc_stats(i))
        i += 1
    return res

@app.route('/data', methods=['POST'])
def addData():
    data = request.get_json()
    db_item = {
        "value": data.get("value"),
        "timestamp": data.get("timestamp"),
        "device_id": data.get("device_id")
    }
    a.add(db_item)
    return "good", 200

@app.route('/graph/<thermometer_id>', methods=['GET'])
def getData(thermometer_id):
    i = thermometer_id
    timestamps = []
    values = []

    data = a.getByQuery({"device_id": str(i)})
    for entry in data:
        t=entry["timestamp"]
        timestamps.append(t)
    
        v=entry["value"]
        values.append(v)
    
    id, min, max, avg= calc_stats(i)

    plt.plot(timestamps, values)
    plt.title("Graph " + str(i))
    plt.xlabel("Timestamp", color="blue")
    plt.ylabel("Values", color="blue")
    plt.subplots_adjust(bottom=0.3)
    plt.text(0.5, -0.2, "min value = "+ str(min) + "\n" + "max value = " + str(max) + "\n" + "avg value = " + str(avg), fontsize=11, ha='center', va='top', transform=plt.subplot().transAxes, multialignment='center')
   
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)
    plt.close()
    return Response(img_bytes, content_type='image/png')
    

@app.route('/', methods=['GET'])
def getLinks():
    endpoints = []
    for rule in app.url_map.iter_rules():
        endpoints.append(str(rule))
    return endpoints

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
