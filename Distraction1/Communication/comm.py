import paho.mqtt.client as mqtt
import os

MQTT_HOST = "10.49.244.103"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 500
MQTT_TOPIC = "server-dist"

# Define on_message event Handler
def on_message(mosq, obj, msg):
	print(msg.payload.decode())
 
# Initiate MQTT Client
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

# Register Event Handlers
mqttc.on_message = on_message

# Connect with MQTT Broker
mqttc.username_pw_set(username = "pi", password = "ECE")
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
mqttc.subscribe(MQTT_TOPIC, 0)

# Message publish function
def publish_message(msg):
    data = 0
    if (msg == "Detected"):
        data = {"To": "Server", "From": "Dist0", "Msg_Type": "Detection"}
    else:
        data = {"To": "Server", "From": "Dist0", "Msg_Type": "Logs", "Msg": msg}
        
    mqttc.publish(MQTT_TOPIC, str(data))

# Main control loop
mqttc.loop_start()

while True:
    publish_message("Detected")
    a = 0
    while a < 500000:
        # Do nothing
        a += 1

# Disconnect from MQTT Broker
mqttc.disconnect()