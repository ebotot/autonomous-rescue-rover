#Ultrasonic Senor Testing & PIR
import RPi.GPIO as GPIO
from gpiozero import MotionSensor
from gpiozero import LED
import time
import threading
#GPIO.setmode(GPIO.BCM)


#motor stuff
#from time import sleep      # Import sleep from time
#import RPi.GPIO as GPIO     # Import Standard GPIO Module

GPIO.setmode(GPIO.BOARD)      # Set GPIO mode to BCM
#GPIO.setwarnings(False);

# PWM Frequency
pwmFreq = 100

# Setup Pins for motor controller
GPIO.setup(19, GPIO.OUT)    # PWMA
GPIO.setup(18, GPIO.OUT)    # AIN2
GPIO.setup(16, GPIO.OUT)    # AIN1
GPIO.setup(22, GPIO.OUT)    # STBY
GPIO.setup(21, GPIO.OUT)    # BIN1
GPIO.setup(23, GPIO.OUT)    # BIN2
GPIO.setup(11, GPIO.OUT)    # PWMB

GPIO.setup(37, GPIO.OUT) #new PWMB aka PWM for servo

servo1 = GPIO.PWM(37,50)

pwma = GPIO.PWM(19, pwmFreq)    
pwmb = GPIO.PWM(11, pwmFreq)    #was 11 before 37
pwma.start(100)
pwmb.start(100)

#Ultrasonic sensor ports
TRIG = 36 #located at gpio16
ECHO = 12 #located at gpio18



#constants
on = 0
off = 1





#GPIO setups
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
#pir = MotionSensor(21) #Infared Sensor port located at gpio21
LED_R = LED(27) #LED port located at gpio27
LED_G = LED(22) #LED port located at gpio22
LED_R.off() #initialize LED to be off
LED_G.off()

# def PIR_thread(): #LED lights up when motion is detected and turns off when undetected
#         print("Motion Measurment In Progress")
#         while True:
#             pir.wait_for_motion()
#             print("Motion Detected")
#             LED_R.on()
#             pir.wait_for_no_motion()
#             LED_R.off()
#             print("Motion Stopped")



## Motor Functions
###############################################################################
def forward(spd):
    runMotor(0, 0, 0)
    runMotor(1, spd, 0)


def reverse(spd):
    runMotor(0, 0, 1)   #motor 0 is front wheels
    runMotor(1, spd, 1) #motor 1 is back wheels

def turnLeft(spd):
    runMotor(0, 50, 0)
    runMotor(1, spd, 1)

def turnRight(spd):
    #runMotor(0, 50, 1)
    #pwma.start(0)
    #pwmb.start(0)
    #pwmSERVO.start(0)
    #time.sleep(1)

    #pwma.ChangeDutyCycle(14) #counter clockwise spin
    #pwmSERVO.ChangeDutyCycle(14) #counter clockwise spin
    #pwmb.ChangeDutyCycle(0.5) #clockwise spin. was 0.5 before
    #time.sleep(0.35) #how long we want the wheel to turn (0.35s is about 270 degrees)
    #pwma.stop()
    #pwmb.stop()
    #pwmSERVO.stop()

    #runMotor(1, spd, 0)
   


#start PWM running, but with value of 0 (pulse off)
    servo1.start(0)
    print ("Waiting for 2 seconds")
    time.sleep(2)

#Let's move the servo!
    print ("Rotating 180 degrees in 10 steps")

# Define variable duty
    duty = 2

# Loop for duty values from 2 to 12 (0 to 180 degrees)
    while duty <= 12:
        servo1.ChangeDutyCycle(duty)
        time.sleep(0.3)
        servo1.ChangeDutyCycle(0)
        time.sleep(0.7)
        duty = duty + 1

# Wait a couple of seconds
    time.sleep(2)

# Turn back to 90 degrees
    print ("Turning back to 90 degrees for 2 seconds")
    servo1.ChangeDutyCycle(7)
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)
    time.sleep(1.5)

#turn back to 0 degrees
    print ("Turning back to 0 degrees")
    servo1.ChangeDutyCycle(2)
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)


   
   

def runMotor(motor, spd, direction):
    GPIO.output(22, GPIO.HIGH);
    in1 = GPIO.HIGH
    in2 = GPIO.LOW

    if(direction == 1):
        in1 = GPIO.LOW
        in2 = GPIO.HIGH

    if(motor == 0):
        GPIO.output(16, in1)
        GPIO.output(18, in2)

    elif(motor == 1):
        GPIO.output(21, in1)
        GPIO.output(23, in2)



def motorStop():
    GPIO.output(22, GPIO.LOW)

#Main
if __name__ == '__main__':
    try:
#         t = threading.Thread(target=PIR_thread)
#         t.daemon = True #thread is killed when program finishes
#         t.start()
        forward(0)
        pulse_start=0
        pulse_end=0
        print("Distance Measurment In Progress")
        while True:
            GPIO.output(TRIG, False)
            print("Waiting for Sensor to Settle...")
            time.sleep(0.2) #change time back up later.

            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)



            while GPIO.input(ECHO)==0:
                pulse_start = time.time()
            while GPIO.input(ECHO)==1:
                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150
            distance = round(distance, 2)
            print("Distance: ", distance, "cm")

            if distance < 30: #set the distance of when the motors should stop
                LED_G.on() #can swtich to motors
                motorStop() # ... stop motor
                turnRight(100)

            else:
                LED_G.off() #can swtich to motors
                forward(35) # run motor forward

    except KeyboardInterrupt: #if there is a keyboardinterrupt (ctrl+c), exit
        print("Cleaning up!")
        LED_R.off()
        GPIO.cleanup()