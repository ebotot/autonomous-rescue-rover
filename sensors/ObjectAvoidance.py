#ObjectAvoidance
import RPi.GPIO as GPIO
from gpiozero import MotionSensor
from gpiozero import LED
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
TRIG = 16 #36 for board
ECHO = 18 #12 for board

#GPIO setups
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
pir = MotionSensor(21) #Infared Sensor port located at gpio21
LED_R = LED(27) #LED port located at gpio27
LED_G = LED(22) #LED port located at gpio22
LED_R.off() #initialize LED to be off
LED_G.off()

#PWM Frequency.. actual_angle = (desried_angle/18 +2)
pwmFreq = 50

#Setup Pins for servo motor        BOARD
GPIO.setup(17, GPIO.OUT)    #PWMB        11

#variable for servo motor
pwmb = GPIO.PWM(17, pwmFreq)   #sensor axle

class Avoidance:
    def __init__(self, direction):
        self.direction = direction

    def sense_right(self):
        print("Moving Sensor 90 degrees to the right")
        pwmb.start(0)
        pwmb.ChangeDutyCycle(2) #90 degree spin
        time.sleep(2)

    def sense_left(self):
        print("Moving sensor 180 degrees to the left")
        pwmb.ChangeDutyCycle(12) #-180 degree spin
        time.sleep(2)

    def sense_front(self):
        print("Moving sensor back to original position")
        pwmb.ChangeDutyCycle(7) #reseting back to original position
        time.sleep(2)
        pwmb.ChangeDutyCycle(0) #keep the motor stable

    def Check_Right_Left(self):
        #checks for right direction
        self.sense_right()
        clear = self.sensor_value()
        if clear is True:
            self.sense_front()
            return "right"
        else:
            #checks for left direction
            self.sense_left()

        clear = self.sensor_value()
        if clear is True:
            self.sense_front()
            return "left"
        else:
            self.sense_front()
            return "reverse"
        return "null"

    def sensor_value(self):
        #this is where the rover recongizes when it is blocked
        object_distance = self.Ultrasonic_data()
        if object_distance <= 10:
            LED_G.on()
            clear = False
        else:
            LED_G.off()
            clear = True
        print("Clear is",clear)
        return clear

    def Ultrasonic_data(self):
        print("Getting Ultrasonic data...")
        pulse_start = 0
        pulse_end = 0
        GPIO.output(TRIG, False)
        time.sleep(0.2) #change time back up later.

        GPIO.output(TRIG, True)
        time.sleep(1)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO)==0:
            pulse_start = time.time()
        while GPIO.input(ECHO)==1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        print("Distance: ", distance, "cm")
        #distance = 8
        return distance
