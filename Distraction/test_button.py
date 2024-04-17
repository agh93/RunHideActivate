import RPi.GPIO as GPIO

testPin0 = 22
testPin1 = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(testPin0, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(testPin1, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def GPIOtest0_callback(channel):
    print("Button " + str(testPin0) + " Pressed")
    
def GPIOtest1_callback(channel):
    print("Button " + str(testPin1) + " Pressed")
    
GPIO.add_event_detect(testPin0, GPIO.FALLING, callback = GPIOtest0_callback, bouncetime = 300)
GPIO.add_event_detect(testPin1, GPIO.FALLING, callback = GPIOtest1_callback, bouncetime = 300)
    
while True:
	a = 1
