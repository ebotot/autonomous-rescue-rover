import RPi.GPIO as GPIO
import lcddriver
from picamera import PiCamera
from time import sleep

GPIO.setmode(GPIO.BCM)

blinkCount = 3
count = 0

### LED for yellow, green and red. Buttons for green (yes) and red (no)
LEDPinY = 26
LEDPinG = 22
LEDPinR = 20
buttonPinG = 5
buttonPinR = 21

### Setup the button
GPIO.setup([buttonPinG, buttonPinR], GPIO.IN, pull_up_down = GPIO.PUD_UP)

### Setup the pin the LED is connected to
GPIO.setup([LEDPinY, LEDPinG, LEDPinR], GPIO.OUT)

### Code internally keeps track of LED and button status
buttonPressG = True
buttonPressR = True
ledStateY = False
ledStateG = False
ledStateR = False

### Load LCD driver to display
display = lcddriver.lcd()

### Load Pi Camera to capture
camera = PiCamera()

try:
	while count < blinkCount:
		GPIO.output(LEDPinY, True)				# Yellow LED on acts like sensor waiting to detect
		print("Asking prompt")					# Prompt status asked in terminal
		display.lcd_display_string("Do you require", 1)		# First line:	14 characters
		display.lcd_display_string("a park ranger?", 2)		# Second line:	14 characters
		buttonPressG = GPIO.input(buttonPinG)			# Detect button press input
		buttonPressR = GPIO.input(buttonPinR)
		if buttonPressG == False and ledStateG == False:	# Green(yes) button is pushed
			GPIO.output(LEDPinY, False)
			GPIO.output(LEDPinG, True)
			ledStateG = True
			print("Yes; Calling ranger")			# Yes in terminal; 2 text lines on LCD
			display.lcd_display_string("[Yes]   Calling", 1)# First line:	16 characters
			display.lcd_display_string("for a ranger", 2)	# Second line:	12 characters
			###camera.start_preview()
			###camera.start_recording('home/pi/Destop/video.h264')	# Pi Camera recording video for 5 seconds
			###sleep(5)
			###camera.stop_recording()
			###camera.stop_preview()
			sleep(4)
			GPIO.output(LEDPinG, False)
			ledStateG = False
		elif buttonPressR == False and ledStateR == True:	# Red (no) button is pushed
			GPIO.output(LEDPinY, False)
			GPIO.output(LEDPinR, True)
			ledStateR = True
			print("No; Leave")				# No in terminal; 2 text lines on LCD
			display.lcd_display_string("[No]", 1)		# First line:	4 characters
			display.lcd_display_string("Enjoy your hike", 2)# Second line:	15 characters
			sleep(4)
			GPIO.output(LEDPinR, False)
			ledStateR = False
		sleep(10)						# Wait 10 seconds before asking question

finally:
	### Reset the GPIO Pins to a safe (off) state and clears LCD of text
	GPIO.cleanup()
	display.lcd_clear()
