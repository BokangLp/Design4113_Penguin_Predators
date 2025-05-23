import os
import time
import RPi.GPIO as GPIO

# Initialise necessary pins (BCM configuration used)
speakerPin =  12
motorPin = 13

# Setting up the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(speakerPin,GPIO.OUT) # PWM for speaker board pin 32 (BCM 12)
GPIO.setup(motorPin, GPIO.OUT) # PWM for motors board pin 33 (BCM 13)

# Drive the speakers using specified frequency(Hz) and duty cycle (as a decimal)
def speakerDrive(frequency,DutyCycle):
	timeON = 1/frequency * DutyCycle	# Calculate time high
	timeOFF = 1/frequency * (1-DutyCycle)	# Calculate time  Low
	GPIO.output(speakerPin,GPIO.HIGH)	# Set pin High
	time.sleep(timeON)			# Wait for a duration of timeON
	GPIO.output(speakerPin,GPIO.LOW)	# Set pin low
	time.sleep(timeOFF)			# wait for ad duration of timeOFF

def motorDrive(frequency,DutyCycle):
	timeON = 1/frequency * DutyCycle
	timeOFF = 1/frequency * (1-DutyCycle)
	GPIO.output(motorPin,GPIO.HIGH)
	time.sleep(timeON)
	GPIO.output(motorPin, GPIO.LOW)
	time.sleep(timeOFF)

if __name__ == "__main__":
	try:
		while True:
			speakerDrive(0.5,0.5)		# 0.5Hz pwm, 50% Duty Cycle
			motorDrive(0.2,0.75)		# 0.2Hz pwm, 75% Duty Cycle
	except KeyboardInterrupt:
		print("Process terminated by user")
	finally:
		GPIO.cleanup()  # Reset GPIO pins to default

