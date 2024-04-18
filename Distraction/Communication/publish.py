import os

MQTT_SERVER = "10.49.243.26"
MQTT_PATH = "testTopic"

msg = 'mosquitto_pub -h ' + str(MQTT_SERVER) + ' -d -t ' + MQTT_PATH + ' -m "HELLO WORLD" -u admin -P ECE'
#os.system('mosquitto_pub -h 10.49.243.26 -d -t testTopic -m "HELLO WORLD" -u admin -P ECE')
os.system(msg)
