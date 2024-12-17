import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT)
pwm6 = GPIO.PWM(6, 100)

pwm6.start(5)

count = 0
while count < 5:
    count += 1
    
    pwm6.ChangeDutyCycle(2.5)
    print("release 1 marble")
    time.sleep(0.07)

    pwm6.ChangeDutyCycle(18.5)
    time.sleep(0.07)

    pwm6.ChangeDutyCycle(0)
    time.sleep(0.1)

pwm6.stop()
print("stop")
GPIO.cleanup()