#Ultrasonic Senor Testing & PIR
import RPi.GPIO as GPIO
from gpiozero import MotionSensor
from gpiozero import LED
import time
import threading
GPIO.setmode(GPIO.BCM)

#Ultrasonic sensor ports
TRIG = 16 #located at gpio16
ECHO = 18 #located at gpio18

#constants
on = 0
off = 1

#GPIO setups
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
pir = MotionSensor(21) #Infared Sensor port located at gpio21
LED_R = LED(27) #LED port located at gpio27
LED_G = LED(22) #LED port located at gpio22
LED_R.off() #initialize LED to be off
LED_G.off()

def PIR_thread(): #LED lights up when motion is detected and turns off when undetected
        print("Motion Measurment In Progress")
        while True:
            pir.wait_for_motion()
            print("Motion Detected")
            LED_R.on()
            pir.wait_for_no_motion()
            LED_R.off()
            print("Motion Stopped")

#Main
if __name__ == '__main__':
    try:
        t = threading.Thread(target=PIR_thread)
        t.daemon = True #thread is killed when program finishes
        t.start()

        print("Distance Measurment In Progress")
        while True:
            GPIO.output(TRIG, False)
            print("Waiting for Senor to Settle...")
            time.sleep(2)

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

            if distance < 8: #set the distance of when the motors should stop
                LED_G.on() #can swtich to motors
            else:
                LED_G.off() #can swtich to motors

    except KeyboardInterrupt: #if there is a keyboardinterrupt (ctrl+c), exit
        print("Cleaning up!")
        LED_R.off()
        GPIO.cleanup()