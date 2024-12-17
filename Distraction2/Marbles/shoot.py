import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

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
        while time.time() < shoot_start + 0.1:
            continue
        
    pwm_servo.stop()
    pwm_shooter.stop()
    
marbles()

#GPIO.cleanup()