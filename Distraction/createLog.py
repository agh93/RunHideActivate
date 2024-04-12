# Ashley Heckman (agh93@cornell.edu)
# createLog.py
# Trigger distraction events TO DO
# Save triggered distraction events in log.txt

import keyboard # remove once server communication working
from datetime import datetime
from time import strftime
from time import time
import random


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
code_started = False
while not code_started:
    if keyboard.is_pressed('p'):
        code_started = True


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

# End condition variables
main_run = True

# Distraction timing variables
prev_distraction_time = 0
wait_time = 0
min_wait_time = 2
max_wait_time = 7

# Enter control loop
while main_run:
      
    # Detect end condition
    # Pressing q on the keyboard will trigger the end event
    # To do: Eventually make this event communication from server
    if keyboard.is_pressed('q'):
        main_run = False

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
        f.write(distraction_str + "\n")
        f.close()

        # Randomize wait time
        wait_time = random.randint(min_wait_time, max_wait_time)


# Indicate unit deactivation in log file
f = open("log.txt", "a")
f.write("\nUnit Deactivated " + get_time_str() + "\n\n\n")
f.close()
