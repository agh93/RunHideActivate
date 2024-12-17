import paho.mqtt.client as mqtt
from datetime import datetime
import RPi.GPIO as GPIO
import subprocess
import neopixel
import random
import board
import time
import ast

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Is the system activated?
system_activated = False

# Has the system detected motion?
motion_detect = False
motion_detect_end = 0

#################################################################################################
# Communication
#################################################################################################

MQTT_HOST = "10.49.244.103"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 500
MQTT_TOPIC = "server-dist"

# Define on_message event Handler
def on_message(mosq, obj, msg):
    global system_activated
    
    # Read the input
    msg_rec = msg.payload.decode()
    msg_dict = ast.literal_eval(msg_rec)
    
    # If distraction devices are the target, update the system status accordingly
    if msg_dict["To"] == "Dist":
        time_str = datetime.now().strftime("%m/%d/%y at %H:%M:%S")
        if msg_dict["Msg_Type"] == "Activation":
            print("system activated")
            system_activated = True
            write_str = "Device Activated " + time_str
            publish_message(write_str)
        else:
            print("system deactivated")
            system_activated = False
            write_str = "Device Deactivated " + time_str
            publish_message(write_str)
 

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
    msg_type = msg.split(' ', 1)[0]
    if (msg == "Detected"):
        data = {"To": "Server", "From": "Dist2", "Msg_Type": "Detection", "Msg": "now"}
    elif (msg == "No Detected"):
        data = {"To": "Server", "From": "Dist2", "Msg_Type": "Detection", "Msg": "prev"}
    elif (msg_type == "Device"):
        data = {"To": "Server", "From": "Dist2", "Msg_Type": "Activation", "Msg": msg}
    else:
        data = {"To": "Server", "From": "Dist2", "Msg_Type": "Logs", "Msg": msg}
        
    mqttc.publish(MQTT_TOPIC, str(data))
    
# Monitor topic
mqttc.loop_start()


#################################################################################################
# Motion
#################################################################################################

# Setup the GPIOs
motion = 4
GPIO.setup(motion, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Motion Detected Callback
def motion_detected(channel):
    
    global motion_detect_end
    global motion_detect
    
    # Only do something if the system is activated
    if system_activated:
    
        # Rising edge
        if GPIO.input(motion):
            
            motion_detect = True
            motion_detect_end = time.time() + 100
            
            print("Motion Detected!")
            
            # Send shooter detected to log file
            time_str = datetime.now().strftime("%m/%d/%y at %H:%M:%S")
            f = open('log.txt', 'a')
            f.write("Shooter Detected: " + time_str + "\n")
            f.close()
            
            # Send shooter detected back to central server
            publish_message("Detected")
            
        # Falling edge
        else:
            motion_detect_end = time.time()
    
    
# Link motion with its callback
GPIO.add_event_detect(motion, GPIO.BOTH, callback=motion_detected)


#################################################################################################
# Marbles
#################################################################################################

# Setup servo for marble release
servo = 6
GPIO.setup(servo, GPIO.OUT)
pwm_servo = GPIO.PWM(servo, 100)

# Setup marble shooter
marble_pwm = 5
marble_go = 19
GPIO.setup(marble_go, GPIO.OUT)
GPIO.setup(marble_pwm, GPIO.OUT)
pwm_shooter = GPIO.PWM(marble_pwm,100)

# Shoot the Marbles
def marbles():
    
    print("marbles")

    # Start up wheels
    pwm_shooter.start(100)
    GPIO.output(marble_go, 1)
    t_start = time.time()
    
    # Wait 5 seconds to allow wheels to reach full speed
    while time.time() < t_start + 5:
        continue
    
    # Release the marbles
    print("shooting")
    pwm_servo.start(5)
    for count in range(6):
        
        pwm_servo.ChangeDutyCycle(2.5)
        shoot_start = time.time()
        while time.time() < shoot_start + 0.13:
            continue

        pwm_servo.ChangeDutyCycle(18.5)
        shoot_start = time.time()
        while time.time() < shoot_start + 0.13:
            continue

        pwm_servo.ChangeDutyCycle(0)
        shoot_start = time.time()
        while time.time() < shoot_start + 0.5:
            continue
        
    pwm_servo.ChangeDutyCycle(0)
    pwm_shooter.ChangeDutyCycle(0)
    

#################################################################################################
# Lights
#################################################################################################

num_lights = 10
pixels = neopixel.NeoPixel(board.D10, num_lights)
light_wait_time = 0.18

def lights():
    
    print("lights")
    
    # clear lights
    pixels.fill((0,0,0))
    
    # Flash police light pattern 5 times
    for count in range(3):
        # Flash halves 3 times
        for num in range(5):

            # Half red
            pixels.fill((0,0,0))
            for i in range(int(num_lights/2)):
                pixels[i + int(num_lights/2)] = (200,0,0)

            # Wait
            light_start = time.time()
            while time.time() < light_start + light_wait_time:
                continue

            # Other half blue
            pixels.fill((0,0,0))
            for i in range(int(num_lights/2)):
                pixels[i] = (0,0,200)

            # Wait
            light_start = time.time()
            while time.time() < light_start + light_wait_time:
                continue


        # Takedown pattern 3 times
        for num in range(5):
            
            # PHASE 1
            # First 2 red
            pixels[9] = (200,0,0)
            pixels[8] = (200,0,0)

            # Next 2 white
            pixels[7] = (200,200,200)
            pixels[6] = (200,200,200)

            # Next 2 black
            pixels[5] = (0,0,0)
            pixels[4] = (0,0,0)

            # Next 2 blue
            pixels[3] = (0,0,200)
            pixels[2] = (0,0,200)

            # Next 2 white
            pixels[1] = (200,200,200)
            pixels[0] = (200,200,200)

            # Wait before next phase
            light_start = time.time()
            while time.time() < light_start + light_wait_time:
                continue


            # PHASE 2
            # First 2 black
            pixels[9] = (0,0,0)
            pixels[8] = (0,0,0)

            # Next 2 white
            pixels[7] = (200,200,200)
            pixels[6] = (200,200,200)

            # Next 2 blue
            pixels[5] = (0,0,200)
            pixels[4] = (0,0,200)

            # Next 2 black
            pixels[3] = (0,0,0)
            pixels[2] = (0,0,0)

            # Next 2 red
            pixels[1] = (200,00,0)
            pixels[0] = (200,0,0)

            # Wait before next phase
            light_start = time.time()
            while time.time() < light_start + light_wait_time:
                continue
    
    # Turn off the lights
    pixels.fill((0,0,0))
    
    
#################################################################################################
# Audio
#################################################################################################

def audio():
    
    print("audio")
    
    # Select random audio file
    # 1 = sirens, 2 = speaking
    audio_num = random.randint(1,2)
    audio_file = False
    
    if audio_num == 1:
        audio_file = "long_siren.wav"
    else:
        audio_file = "a-team_con_man.wav"
        
    # Start aplay
    aplay_process = subprocess.Popen(["aplay", audio_file])
    
    # Play for 7 seconds
    audio_start = time.time()
    while time.time() < audio_start + 7:
        continue
    
    # Stop aplay
    aplay_process.terminate()
    
    
    
#################################################################################################
# Program Control Loop
#################################################################################################

# Loop to keep program running
code_run = True
while code_run:
	
    # Loop for activated state
    while system_activated:
        
        # If motion was detected in the last 10 seconds, deploy distractions
        if motion_detect and time.time() < motion_detect_end + 30:
        
            # Wait a random amount of time (5-10 seconds)
            wait_time = random.randint(5, 10)
            print("waiting " + str(wait_time) + " seconds")
            wait_start = time.time()
            
            while time.time() < wait_start + wait_time:
                continue
            
            # Select a random distraction
            # 1 = lights, 2 = marbles, 3 = audio
            dist = random.randint(2,3)
            
            # Deploy the proper distraction and communicate as needed
            if system_activated:
                
                if dist == 1:
                    # Send lights to log file
                    time_str = datetime.now().strftime("%m/%d/%y at %H:%M:%S")
                    write_str = "Lights    " + time_str
                    f = open('log.txt', 'a')
                    f.write(write_str + "\n")
                    f.close()
                    
                    # Also send lights to server
                    publish_message(write_str)
                    
                    # Deploy the lights
                    lights()
                    
                elif dist == 2:
                    # Send marbles to log file
                    time_str = datetime.now().strftime("%m/%d/%y at %H:%M:%S")
                    write_str = "Marbles   " + time_str
                    f = open('log.txt', 'a')
                    f.write(write_str + "\n")
                    f.close()
                    
                    # Also send lights to server
                    publish_message(write_str)
                    
                    # Deploy the marbles
                    marbles()
                    
                else:
                    
                    # Send audio to log file
                    time_str = datetime.now().strftime("%m/%d/%y at %H:%M:%S")
                    write_str = "Audio     " + time_str
                    f = open('log.txt', 'a')
                    f.write(write_str + "\n")
                    f.close()
                    
                    # Also send audio to server
                    publish_message(write_str)
                    
                    # Deploy the audio
                    audio()
                    
                    
        # Send signal indicating that motion is no longer detected here
        elif motion_detect:
            print("no longer detected")
            publish_message("No Detected")
            motion_detect = 0
        

# Cleanup the GPIOs
GPIO.cleanup()
