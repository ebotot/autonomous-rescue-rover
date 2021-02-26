import RPi.GPIO as GPIO
import lcddriver
from pygame import mixer
import threading
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) # Disable warnings

### Load pygame.mixer to play audio
mixer.init()

### Load LCD driver to display
display = lcddriver.lcd()

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

### Setup GPIO input buttons
BTN_G = 25              # Pin22, GPIO 25 - Green Button

GPIO.setup(BTN_G, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

def distanceLCD():
	display.lcd_clear()
        display.lcd_display_string("Distance :", 1)
        result = str(distance)+" cm"
        display.lcd_display_string(result, 2);

def interface(): 
	display.lcd_clear()
	print("Asking prompt")					# Prompt status asked in terminal
	
	display.lcd_display_string("Do you require", 1)		# First line:   14 characters
	display.lcd_display_string("a park ranger?", 2)		# Second line:  14 characters
	
	mixer.music.load('/home/pi/components/lcd/1_Prompt_Female.wav')
	mixer.music.play()
	time.sleep(3)
	
	print("Ready for answer")
	
	GPIO.wait_for_edge(BTN_G, GPIO.RISING, timeout = 5000)
	if (GPIO.input(BTN_G)):
		print("Yes; Calling ranger")				# Yes in terminal; 2 text lines on LCD
		
		display.lcd_clear()
		display.lcd_display_string("[Yes]   Calling", 1)	# First line:   16 characters
		display.lcd_display_string("for a ranger", 2)		# Second line:  12 characters
		
		mixer.music.load('/home/pi/components/lcd/2_AnswerYes_Female.wav')
		mixer.music.play()
		time.sleep(3)
	else:
		print("No; Leave")					# No in terminal; 2 text lines on LCD
		
		display.lcd_clear()
		display.lcd_display_string("[No]", 1)           # First line:   4 characters
		display.lcd_display_string("Enjoy your hike", 2)# Second line:  15 characters
		
		mixer.music.load('/home/pi/components/lcd/2_AnswerNo_Female.wav')
		mixer.music.play()
		time.sleep(1)
		
		time.sleep(3)
	
	
except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press Ctrl+C)
	print("\nCleaning up interface!") # exit the program and cleanup
	GPIO.cleanup()
	display.lcd_clear()
