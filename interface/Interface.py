import RPi.GPIO as GPIO
import lcddriver
from picamera import PiCamera
import pygame
import time
import threading
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) # Disable warnings

### Load pygame to play audio
pygame.init()

### Load LCD driver to display
display = lcddriver.lcd()

### Load Pi Camera to capture
camera = PiCamera()

### Set I/O Pins for Ultrasonic Sensor
TRIG = 23
ECHO = 24

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

### Setup GPIO input buttons and output LEDs
BTN_G = 25              # Pin22, GPIO 25 - Green Button
BTN_R = 18              # Pin12, GPIO 18 - Red Button

LED_G = 5               # Pin29, GPIO 5 - Green LED
LED_R = 6               # Pin31, GPIO 6 - Red LED

BTN2LED = {
    BTN_G: LED_G,
    BTN_R: LED_R,}

GPIO.setup([BTN_G, BTN_R], GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup([LED_G, LED_R], GPIO.OUT, initial = GPIO.LOW)

try:
    while True:
        
        
        GPIO.output(TRIG, False)
        print "Waiting For Sensor To Settle"
        
        time.sleep(2)
        
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        
        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()
        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()
        
        pulse_duration = pulse_end - pulse_start
        
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        
        display.lcd_clear()
        display.lcd_display_string("Distance :", 1)
        result = str(distance)+" cm"
        display.lcd_display_string(result, 2);
        
        if distance < 20:
            display.lcd_clear()
            print("Asking prompt")                              # Prompt status asked in terminal
            display.lcd_display_string("Do you require", 1)     # First line:   14 characters
            display.lcd_display_string("a park ranger?", 2)     # Second line:  14 characters
            pygame.mixer.music.load("1_Prompt_Female.wav")
            pygame.mixer.music.play()
            time.sleep(2)
	
            if GPIO.input(BTN_G):
                GPIO.output(LED_G, True)
                print("Yes; Calling ranger")                        # Yes in terminal; 2 text lines on LCD
                display.lcd_clear()
                display.lcd_display_string("[Yes]   Calling", 1)    # First line:   16 characters
                display.lcd_display_string("for a ranger", 2)       # Second line:  12 characters
		pygame.mixer.music.load("2_AnswerYes_Female.wav")
		pygame.mixer.music.play()
                camera.start_preview()                              # Start camera view
                time.sleep(5)
                camera.stop_preview()
            elif GPIO.input(BTN_R):
                GPIO.output(LED_R, True)
                print("No; Leave")                              # No in terminal; 2 text lines on LCD
                display.lcd_clear()
                display.lcd_display_string("[No]", 1)           # First line:   4 characters
                display.lcd_display_string("Enjoy your hike", 2)# Second line:  15 characters
		pygame.mixer.music.load("2_AnswerNo_Female.wav")
		pygame.mixer.music.play()

        time.sleep(3)
        GPIO.output([LED_G, LED_R], True)
        
        
except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press Ctrl+C)
    print("Cleaning up!") # exit the program and cleanup
    GPIO.output([LED_G, LED_R], False)
    GPIO.cleanup()
    display.lcd_clear()
