## To Startup Server
flask --app flask_app run --host=<ip address for ssh, rn is 10.49.244.103>

## To Startup Distraction Devices
Ensure that MQTT_HOST in distraction.py is the server address (same as in command above)

sudo python3 distraction.py
