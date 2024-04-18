import os

MQTT_PATH = "testTopic"

msg = 'mosquitto_sub -d -t ' + MQTT_PATH + ' -u admin -P ECE'
os.system(msg)
