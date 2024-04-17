# Ashley Heckman (agh93@cornell.edu)
# createLog.py
# Trigger distraction events TO DO
# Save triggered distraction events in log.txt

import RPi.GPIO as GPIO
from time import strftime
from time import time
from datetime import datetime
import random


# =================================================================================
# GPIO callbacks
# =================================================================================
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_UP)

code_started = False
def GPIO27_callback(channel):
    global code_started
    code_started = True
    print("Button 27 Pressed")

main_run = True
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

# Pressing p on the keyboard will trigger the start event
# To do: Eventually make this event communication from server
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
GPIO.cleanup()
