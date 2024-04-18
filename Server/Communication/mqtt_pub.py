import paho.mqtt.client as mqtt
import os

MQTT_HOST = "10.49.243.26"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 500
MQTT_TOPIC = "testing"
MQTT_MSG = "Hello Test"

# Define on_connect event Handler
def on_connect(mosq, obj, rc):
	print("Connected to MQTT Broker")

# Define on_publish event Handler
def on_publish(client, userdata, mid):
	print("Message Published...")

# Initiate MQTT Client
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

# Register Event Handlers
mqttc.on_publish = on_publish
mqttc.on_connect = on_connect

# Connect with MQTT Broker
mqttc.username_pw_set(username = "admin", password = "ECE")
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)

# Main control loop
code_run = True
while code_run:

	# Get user input
	MQTT_MSG = input("Enter message to send: ")

	# Publish message to MQTT Topic
	mqttc.publish(MQTT_TOPIC, MQTT_MSG)

	# If message was stop, exit this loop
	if MQTT_MSG == "Stop":
		code_run = False

# Disconnect from MQTT Broker
mqttc.disconnect()