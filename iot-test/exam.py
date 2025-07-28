import json
from flask import Flask, request, jsonify

from time import time
from bson import json_util
from bson.objectid import ObjectId
from pymongo import MongoClient

app = Flask(__name__)

DATABASE_NAME = "mongo_exam_database"

# ------------------------------------------------------------------------------------------------
# Заменете с вашия connection string
CONNECTION_STRING = "mongodb+srv://ilievayana:iylfRpWikjic485Y@cluster0.ij9wh5k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


# Да се създаде нов сензор в колекцията за сензори на вашата база от данни.
# Заявката приема JSON тяло с информация за сензора.
# Заявката връща новосъздадения сензор.
@app.route("/sensors", methods=["POST"])
def create_air_quality_sensor():
    data = request.get_json()
    s = {
        "city": data.get("city"),
        "type": data.get("type")
    }
    air_quality_sensor_collection.insert_one(s)
    return jsonify(json.loads(json_util.dumps(s))), 201



# Да се промени информацията за даден сензор.
# Заявката приема JSON тяло с нова информация за сензора.
# Заявката връща променения сензор.
@app.route("/sensors/<sensor_id>", methods=["PUT"])
def update_air_quality_sensor(sensor_id):
    s = air_quality_sensor_collection.find_one({"_id": ObjectId(sensor_id)})
    if s:
        data = request.get_json()
        s = {
        "city": data.get("city"),
        "type": data.get("type")
        }
        air_quality_sensor_collection.update_one({"_id": ObjectId(sensor_id)}, {"$set": s})
        return jsonify(json.loads(json_util.dumps(s))), 200
    else:
        return jsonify({"error":"no sensor"}), 404


# Да се изтрие информацията за даден сензор.
# Заявката не приема тяло.
# Заявката връща информация дали изтриването е било успешно.
@app.route("/sensors/<sensor_id>", methods=["DELETE"])
def delete_sensor(sensor_id):
    s = air_quality_sensor_collection.find_one({"_id": ObjectId(sensor_id)})
    if s:
        air_quality_sensor_collection.delete_one({"_id": ObjectId(sensor_id)})
        return "",204
    else: 
        return jsonify({"error":"no sensor"}), 404


# Да се добави информация за получени данни от съответен сензор.
# Заявката приема JSON тяло.
# Заявката връща новосъздадения запис.
@app.route("/sensors/<sensor_id>/data", methods=["POST"])
def create_air_quality_sensor_data_entry(sensor_id):
    data2 = request.get_json()
    data = {
        "sensor_id": ObjectId(sensor_id),
        "timestamp":data2.get("timestamp"),
        "value": data2.get("value")
    }
    air_quality_sensor_data_collection.insert_one(data)
    return jsonify(json.loads(json_util.dumps(data))), 201


# Да се изтрие записана информация за получени данни.
# Заявката не приема тяло.
# Заявката връща информация дали изтриването е било успешно
@app.route("/sensors/<sensor_id>/data/<data_id>", methods=["DELETE"])
def delete_air_quality_sensor_data_entry(sensor_id, data_id):
    data = air_quality_sensor_data_collection.find_one({"sensor_id": ObjectId(sensor_id), "_id": ObjectId(data_id)})
    if data:
        air_quality_sensor_collection.delete_one({"_id": ObjectId(data_id)})
        return "", 204
    else:
        return jsonify({"error":"no sensor"}), 404

# Да се върне информацията за съответния сензор.
# Заявката не приема тяло.
# Заявката връща документа на сензора.
@app.route("/sensors/<sensor_id>", methods=["GET"])
def get_air_quality_sensor_by_id(sensor_id):
    s = air_quality_sensor_collection.find_one({"_id": ObjectId(sensor_id)})
    if s:
        return jsonify(json.loads(json_util.dumps(s))), 200
    else: return jsonify({"error":"no sensor"}), 404



# Да се върнат всички сензори от даден тип сортирани по град в низходящ ред.
# Заявката не приема тяло.
# Заявката връща списък с правилно подредени сензори.
@app.route("/sensors/type/<type>", methods=["GET"])
def get_air_quality_sensor_by_type_sorted_by_city_descending(type):
    s = air_quality_sensor_collection.find({"type": type}).sort("city", -1)
    return jsonify(json.loads(json_util.dumps(s))), 201


# Да се върне средно аритметично на всички стойности, отчетени от даден сензор.
# Заявката не приема тяло.
# Заявката връща средноаритметичната стойност за дадения сензор.
@app.route("/sensors/<sensor_id>/average", methods=["GET"])
def get_average_air_quality_by_sensor(sensor_id):
    data = air_quality_sensor_data_collection.find_one({"_id": ObjectId(sensor_id)}, {"_id": 0, "value":1})
    values = [entry ["value"] for entry in data]

    if values:
        avg = sum(values) /len(values)
    # if data and "value" in data:
    #     avg = sum(data["value"]) / len(data["value"])
        return jsonify(json.loads(json_util.dumps(avg))), 200
    else:
        return jsonify({"error": "no sensor"}), 404


# Да се върнат всички отчетени стойности над посочената стойност <value> за даден сензор.
# Заявката не приема тяло.
# Заявката връща списък с всички отчетени стойности над определената стойност <value> за подадения сензор.
@app.route("/sensors/<sensor_id>/data/filter/<value>", methods=["GET"])
def get_air_quality_sensor_data_above_value(sensor_id, value):
    data = air_quality_sensor_collection.find({"sensor_id": ObjectId(sensor_id ), "value": {"$gt": int(value)}})

    filtered = [entry for entry in data]
    if filtered:
        return jsonify(json.loads(json_util.dumps(filtered))), 200
    else:
        return jsonify({"error": "No data found for this sensor and value"}), 404



# Да се върнат последните отчетени <n> на брой стойности за даден сензор.
# Заявката не приема тяло.
# Заявката връща списък с последните <n> на брой стойности за дадения сензор.
@app.route("/sensors/<sensor_id>/data/limit/<n>", methods=["GET"])
def get_air_quality_sensor_data_last_n_entries(sensor_id, n):
    data = air_quality_sensor_data_collection.find({"sensor_id": ObjectId(sensor_id)}, {"_id": 0}).sort([("timestamp", -1)]).limit(int(n))

    limited = [entry for entry in data]
    # return jsonify(json.loads(json_util.dumps(data))), 200
    if limited:
        return jsonify(json.loads(json_util.dumps(limited))), 200
    else:
        return jsonify({"error": "No data found for this sensor"}), 404



# -----------------------------------------------------------------------------------------------

def get_database():
    # create a connection using MongoClient
    mongo_client = MongoClient(CONNECTION_STRING)

    # return the database
    return mongo_client.get_database(DATABASE_NAME)


if __name__ == "__main__":
    database = get_database()
    air_quality_sensor_collection = database.get_collection("air_quality_sensors")
    air_quality_sensor_data_collection = database.get_collection("air_quality_sensor_data")
    app.run(debug=True, port=8000)