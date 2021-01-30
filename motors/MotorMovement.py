#MotorMovement
import RPi.GPIO as GPIO  # Import Standard GPIO Module
from gpiozero import MotionSensor
from gpiozero import LED
from time import sleep      # Import sleep from time

GPIO.setmode(GPIO.BCM)      # Set GPIO mode to BCM
GPIO.setwarnings(False);

#PWM Frequency.. actual_angle = (desried_angle/18 +2)
pwmFreq = 50

#Setup Pins for motor controller        BOARD
GPIO.setup(4, GPIO.OUT)    #PWMA         7
GPIO.setup(24, GPIO.OUT)    #AIN2        18
GPIO.setup(23, GPIO.OUT)    #AIN1        16
GPIO.setup(25, GPIO.OUT)    #STBY        22
GPIO.setup(9, GPIO.OUT)    #BIN1        21
GPIO.setup(11, GPIO.OUT)    #BIN2        23

#variable for servo motor
pwma = GPIO.PWM(4, pwmFreq)    #front wheel axis


class Move:
    def __init__(self, movement, spd):
        self.movement = movement
        self.spd = spd

    def forward(self, spd):
        print("Rover moving forward with %s power." % (spd))
        in1 = GPIO.LOW
        in2 = GPIO.HIGH

        #front wheels
        GPIO.output(23, in1)
        GPIO.output(24, in2)
        #back wheels
        GPIO.output(9, in1)
        GPIO.output(11, in2)

    def reverse(self, spd):
        print("Normalizing the reverse path")
        in1 = GPIO.LOW
        in2 = GPIO.HIGH

        #front wheels
        GPIO.output(23, in1)
        GPIO.output(24, in2)
        #back wheels
        GPIO.output(9, in1)
        GPIO.output(11, in2)

    def right(self):
        print("Normalizing the right turn path")
        pwma.start(0)
        pwma.ChangeDutyCycle(6) #+15 degrees spin
        sleep(1)
        pwma.ChangeDutyCycle(0) #keep the motor stable

        #run the motor forward for a bit
        self.forward(self.spd)
        sleep(2)
        self.motorStop()
        pwma.ChangeDutyCycle(7) #reseting back to original position
        sleep(1)
        pwma.ChangeDutyCycle(0) #keep the motor stable


    def left(self):
        print("Normalizing the left turn path")
        pwma.start(0)
        pwma.ChangeDutyCycle(8) #initialize motor
        sleep(1)
        pwma.ChangeDutyCycle(0) #keep the motor stable

        #run motor forward for a bit
        self.forward(self.spd)
        sleep(2)
        self.motorStop()
        pwma.ChangeDutyCycle(7) #reseting back to original position
        sleep(1)
        pwma.ChangeDutyCycle(0) #keep the motor stable

    def motorStop(self):
        print("Motors have stopped")
        GPIO.output(25, GPIO.LOW)

    def runMotor(self, movement, spd):
        print("running motor...")
        GPIO.output(25, GPIO.HIGH);
        if(movement is "forward"):
            self.forward(self.spd)

        elif(movement is "left"):
            self.left()
            return

        elif(movement is "right"):
            self.right()
            return

        elif(movement is "reverse"):
            self.reverse(self.spd)
            self.movement = "forward" #try going forward again

        else:
            #when the movement is halted
            print("Continue")

        return









