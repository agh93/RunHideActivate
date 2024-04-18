# Ashley Heckman (agh93@cornell.edu)
# createLog.py
# Trigger distraction events TO DO
# Save triggered distraction events in log.txt

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from time import strftime
from time import time
from datetime import datetime
import random
import paramiko

# ================================================================================
# MQTT Communication Stuff
# ================================================================================
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
code_started = False
main_run = True
def on_message(mosq, obj, msg):

    # Got activation signal, start the code
    global code_started
    if msg.payload.decode() == "Activate":
        print("Distraction Device Activated")
        code_started = True

    # Got deactivation signal, stop the code
    global main_run
    if msg.payload.decode() == "Stop":
        print("Distraction Device Deactivated")
        main_run = False

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
mqttc.loop_start()


# =================================================================================
# GPIO callbacks
# =================================================================================
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def GPIO27_callback(channel):
    global code_started
    code_started = True
    print("Button 27 Pressed")

def GPIO22_callback(channel):
    global main_run
    main_run = False
    print("Button 22 Pressed")
    
GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=300)
GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=300)


# =================================================================================
# Helper functions
# =================================================================================

# Get current time string
def get_time_str():
    return datetime.now().strftime("%m/%d/%y at %H:%M:%S")


# =================================================================================
# Start Event
# =================================================================================
# Detect device activation event and update the log file accordingly

# On "Activate" signal from server, trigger the start event (exit this loop)
while not code_started:
    continue


# Indicate when the device was activated
# Open log file and add today's date and time
f = open("log.txt", "a")
f.write("============================================================\n")
f.write("Unit Activated " + get_time_str() + "\n")
f.write("============================================================\n\n")
f.close()


# =================================================================================
# Main control loop
# =================================================================================
# Trigger distractions at random times, randomly select from list of distractions
# Detect deactivate condition

# Distraction timing variables
prev_distraction_time = 0
wait_time = 0
min_wait_time = 2
max_wait_time = 7

# Enter control loop
while main_run:

    # Trigger a distraction if we've exceeded the wait time
    # Once distraction is triggered, randomize wait time
    if time() > prev_distraction_time + wait_time:

        # Distraction Trigger/Activation
        # Select random distraction
        # To Do: Implement distraction gpios
        distraction = random.randint(0,2)

        # Update distraction trigger time
        prev_distraction_time = time()

        # Save to log file
        f = open("log.txt", "a")
        distraction_str = ("Noise     " if distraction == 0 else ("Marbles   " if distraction == 1 else "Confetti  ")) + get_time_str()
        print(distraction_str)
        f.write(distraction_str + "\n")
        f.close()

        # Randomize wait time
        wait_time = random.randint(min_wait_time, max_wait_time)


# Indicate unit deactivation in log file
f = open("log.txt", "a")
f.write("\nUnit Deactivated " + get_time_str() + "\n\n\n")
f.close()

# Stop the mqtt communication
mqttc.loop_stop()

# Cleanup the GPIOs
GPIO.cleanup()

# Copy the log file to the server
scp_client = paramiko.SSHClient()
scp_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
scp_client.connect(MQTT_HOST, username='pi',password='ECE')
sftp = scp_client.open_sftp() 
sftp.put("/home/pi/RunHideActivate/Distraction/log.txt", "/home/pi/RunHideActivate/Server/dist0_log.txt")
sftp.close()