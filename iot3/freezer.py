import json
import time
import threading

class Freezer:
    def __init__(self, thing_id, freezer_number):
        self.thing_id = self.policy_id = thing_id
        self.file_name = thing_id + ".json"
        self.event = threading.Event()
        self.attributes = {
            "manufacturer": "Samsung",
            "number": freezer_number,
        }
        self.features = {
            "temperatureControl": {
                "properties": {
                    "temperature": -20,
                    "humidity": 50
                },
                "desiredProperties": {
                    "temperature": -19
                }
            },

            "state": {
                "properties": {
                    "working": True
                }
            },
        }

    def save_to_json(self):
        # Collect all class attributes needed for serialization
        serializable = {
            "thingId": self.thing_id,
            "policyId": self.policy_id,
            "attributes": self.attributes,
            "features": self.features
        }
        # Open file with writing mode (delete everything in it beforehand)
        with open("./digital-twins/" + self.file_name, 'w') as output:
            json.dump(serializable, output, indent=4, ensure_ascii=False)

    def break_freezer(self):
        # Break freezer
        print("Freezer number " + str(self.attributes["number"]) + " is broken")
        self.features["state"]["properties"]["working"] = False
        self.features["temperatureControl"]["properties"]["temperature"] += 20
        self.save_to_json()

    def fix_freezer(self, tech_id):
        # Technician is fixing freezer
        print("Technician " + str(tech_id) + " is fixing freezer number " + str(self.attributes["number"]))
        time.sleep(5)
        print("Freezer number " + str(self.attributes["number"]) + " is fixed")
        self.features["state"]["properties"]["working"] = True
        self.save_to_json()

    def update_temperature_control(self, temperature, humidity):
        # Receive data
        self.features["temperatureControl"]["properties"]["temperature"] = temperature
        self.features["temperatureControl"]["properties"]["humidity"] = humidity
        print("Update from freezer " + str(self.attributes["number"]) + ": temperature: " + str(temperature) + ", humidity: " + str(humidity))
        self.save_to_json()