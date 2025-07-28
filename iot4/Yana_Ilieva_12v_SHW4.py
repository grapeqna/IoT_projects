import paho.mqtt.client as mqtt
import random

player_one = 'Nadya'
player_two = 'Iva'

MQTT_CLIENT_ID          = f"iot4-tictactoe-player{random.randint(0, 6969696969)}"
MQTT_BROKER             = "broker.mqttdashboard.com"
MQTT_TOPIC_MOVE_ONE     = "iot4-tictactoe/player/1"
MQTT_TOPIC_MOVE_TWO     = "iot4-tictactoe/player/2"
MQTT_RESPONSE_ONE_TOPIC = "iot4-tictactoe/response/1"
MQTT_RESPONSE_TWO_TOPIC = "iot4-tictactoe/response/2"

def response(client, userdata, flag):
    print(str(flag.payload.decode()))

client = mqtt.Client(client_id = MQTT_CLIENT_ID)
client.on_message = response
client.connect(MQTT_BROKER, 1883, 60)

client.loop_start()

try:
    name = input('What is your name sweetie?\n')
    
    if name == 'Nadya':
        client.subscribe(MQTT_RESPONSE_ONE_TOPIC)

    elif name == 'Iva':
        client.subscribe(MQTT_RESPONSE_TWO_TOPIC)

    while True:
        info = input('Write it in this order: name column(-1),row(-1)\n')
        info = info.split(' ')

        if info[0] == player_one:
            client.publish(MQTT_TOPIC_MOVE_ONE, info[1])

        elif info[0] == player_two:
            client.publish(MQTT_TOPIC_MOVE_TWO, info[1])

finally:
    client.loop_stop()
    client.disconnect()