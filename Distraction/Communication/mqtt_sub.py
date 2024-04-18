import paho.mqtt.client as mqtt

MQTT_HOST = "10.49.243.26"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 500
MQTT_TOPIC = "testing"

# Define on_connect event Handler
def on_connect(mosq, obj, flags, rc):
	# Subscribe to the Topic
	mqttc.subscribe(MQTT_TOPIC, 0)

# Define on_subscribe event Handler
def on_subscribe(mosq, obj, mid, granted_qos):
	print("Subscribed to MQTT Topic")

# Define on_message event Handler
def on_message(mosq, obj, msg):
	print(msg.payload.decode())

# Initiate MQTT Client
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

# Register Event Handlers
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

# Connect with MQTT Broker
mqttc.username_pw_set(username = "admin", password = "ECE")
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)

# Continue to network loop
mqttc.loop_forever()
