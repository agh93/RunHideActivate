from flask import Flask, render_template, request, send_from_directory
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import paho.mqtt.client as mqtt
from PIL import Image
import os
import ast

#################################################################################################
# Map
#################################################################################################

dist1_status = "clear"
dist2_status = "clear"

def update_map(status1, status2):
    
    # Color codes
    s_r = '#ff0019'
    s_b = '#143ffd'
    s_g = '#28a745'

    # Open the map and create the "new" image
    im = Image.open('maps/map1.png')
    fig, ax = plt.subplots()

    # Display the image without axis numbers or bordering box
    ax.imshow(im)
    plt.xticks([])
    plt.yticks([])
    plt.box(False)
    
    # Box 1 color
    c1 = 0
    if status1 == "now":
        c1 = s_r
    elif status1 == "prev":
        c1 = s_b
    else:
        c1 = s_g
        
    # Box 2 color
    c2 = 0
    if status2 == "now":
        c2 = s_r
    elif status2 == "prev":
        c2 = s_b
    else:
        c2 = s_g

    # Color the rectangle and add it to the map
    rect1 = patches.Rectangle((380, 560), 30, 30, linewidth=1, edgecolor=c1, facecolor=c1)
    rect2 = patches.Rectangle((380, 375), 30, 30, linewidth=1, edgecolor=c2, facecolor=c2)
    ax.add_patch(rect1)
    ax.add_patch(rect2)
    
    # Save the map
    plt.savefig("/home/pi/PROJ/maps/map1_colorized.png")


#################################################################################################
# Communication
#################################################################################################

MQTT_HOST = "localhost"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 500
MQTT_TOPIC = "server-dist"

# Define on_connect event Handler
def on_connect(mosq, obj, flags, rc):
	print("Connected to MQTT Broker")
 
# Define on_publish event Handler
def on_publish(client, userdata, mid):
	print("Message Published...")
 
# Define on_subscribe event Handler
def on_subscribe(mosq, obj, mid, granted_qos):
	print("Subscribed to MQTT Topic")

# Define on_message event Handler
def on_message(mosq, obj, msg):
    
    # Read the input
    msg_rec = msg.payload.decode()
    msg_dict = ast.literal_eval(msg_rec)
    
    # Check for signals to central server
    if msg_dict["To"] == "Server":
        
        # Check for shooter detection
        global dist2_status
        global dist1_status
        if msg_dict["Msg_Type"] == "Detection":
            detect_str = msg_dict["Msg"]
            if msg_dict["From"] == "Dist1":
                dist1_status = detect_str
                update_map(dist1_status, dist2_status)
            else:
                dist2_status = detect_str
                update_map(dist1_status, dist2_status)
                
        # Check for log file signals
        elif msg_dict["Msg_Type"] == "Logs":
            log_str = msg_dict["Msg"]
            if msg_dict["From"] == "Dist1":
                f = open('/home/pi/PROJ/logs/device1_log.txt', 'a')
                f.write(log_str + "\n")
                f.close()
            else:
                f = open('/home/pi/PROJ/logs/device2_log.txt', 'a')
                f.write(log_str + "\n")
                f.close()
                
        # Check for distraction activation/deactivation
        elif msg_dict["Msg_Type"] == "Activation":
            activate_str = msg_dict["Msg"]
            if msg_dict["From"] == "Dist1":
                f = open('/home/pi/PROJ/logs/device1_log.txt', 'a')
                f.write("\n============================================================\n")
                f.write(str(activate_str) + "\n")
                f.write("============================================================\n\n")
                f.close()
            else:
                f = open('/home/pi/PROJ/logs/device2_log.txt', 'a')
                f.write("\n")
                f.write("\n============================================================\n")
                f.write(str(activate_str) + "\n")
                f.write("============================================================\n\n")
                f.write("\n")
                f.close()
                
 
# Initiate MQTT Client
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

# Register Event Handlers
mqttc.on_publish = on_publish
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message

# Connect with MQTT Broker
mqttc.username_pw_set(username = "pi", password = "ECE")
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
mqttc.subscribe(MQTT_TOPIC, 0)

# Watch the topic for new messages
mqttc.loop_start()


#################################################################################################
# Flask
#################################################################################################

app = Flask(__name__)

# Define the path to the logs folder
LOGS_FOLDER = os.path.join(os.getcwd(), 'logs')
MAPS_FOLDER = os.path.join(os.getcwd(), 'maps')

# Keep track of system status (online, offline, activated)
SYSTEM_STATUS = 'Online'

# Route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password are correct
        if username == 'admin' and password == 'ECE':
            return render_template('server.html', system_status=SYSTEM_STATUS)
        else:
            error = "Invalid username or password!"
    
    return render_template('login.html', error=error)


# Route for serving log files
@app.route('/logs/<filename>')
def serve_log(filename):
    if filename not in ['device1_log.txt', 'device2_log.txt']:
        return "File not found", 404
    return send_from_directory(LOGS_FOLDER, filename)

# Route for serving map files
@app.route('/maps/<filename>')
def serve_map(filename):
    if filename not in ['map1.png', 'map1_colorized.png']:
        return "File not found", 404
    return send_from_directory(MAPS_FOLDER, filename)

# Update based on system activation/deactivation
@app.route('/slider_update', methods=['POST'])
def slider_update():
    global SYSTEM_STATUS
    
    # Read system status
    stat = request.data.decode('utf-8')
    status = ast.literal_eval(stat)
    
    # Activate the system - send a message to the distraction devices
    if status["status"] == 'activated':
        SYSTEM_STATUS = 'Activated'
        data = {"To": "Dist", "From": "Server", "Msg_Type": "Activation"}
        mqttc.publish(MQTT_TOPIC, str(data))
    
    # Deactivate the system - send a message to the distraction devices
    else:
        global dist1_status
        global dist2_status
        dist1_status = "clear"
        dist2_status = "clear"
        update_map(dist1_status, dist2_status)
        SYSTEM_STATUS = 'Online'
        data = {"To": "Dist", "From": "Server", "Msg_Type": "DeActivation"}
        mqttc.publish(MQTT_TOPIC, str(data))
        
    # Update html display to reflect new system status
    return render_template('server.html', system_status=SYSTEM_STATUS)


if __name__ == '__main__':
    app.run()
