import RPi.GPIO as GPIO
import os

# Play sirens
def play_sound(channel):
	print("Motion Detected!")
	os.system("aplay /home/pi/PROJ/Audio/long_siren.wav")

# Read GPIO 4 - Motion Pin
motion = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(motion, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(motion, GPIO.RISING, callback=play_sound)

# Loop to keep program running
# Exit when user inputs 0 (deactivation signal)
code_run = True
while code_run:
	code_run = int(input("Enter 0 to stop at anytime\n\n"))

# Stop aplayer
os.system("kill $(ps | grep aplay | cut -d\" \" -f2)")

# Cleanup the GPIOs
GPIO.cleanup()
