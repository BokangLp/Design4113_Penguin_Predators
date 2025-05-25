import time
import RPi.GPIO as GPIO

# Drive the speakers using specified frequency(Hz) and duty cycle (as a decimal)
def speakerDrive(frequency,DutyCycle,speaker_Pin):
	timeON = 1/frequency * DutyCycle	# Calculate time high
	timeOFF = 1/frequency * (1-DutyCycle)	# Calculate time  Low
	GPIO.output(speaker_Pin,GPIO.HIGH)	# Set pin High
	time.sleep(timeON)			# Wait for a duration of timeON
	GPIO.output(speaker_Pin,GPIO.LOW)	# Set pin low
	time.sleep(timeOFF)			# wait for ad duration of timeOFF

def ledDrive(frequency,DutyCycle,LED_Pin):
	timeON = 1/frequency * DutyCycle
	timeOFF = 1/frequency * (1-DutyCycle)
	GPIO.output(LED_Pin,GPIO.HIGH)
	time.sleep(timeON)
	GPIO.output(LED_Pin, GPIO.LOW)
	time.sleep(timeOFF)

def motorDrive(motor_pin):
	GPIO.output(motor_pin,GPIO.HIGH)

if __name__ == "__main__":
	try:
		while True:
			speakerDrive(0.5,0.5)		# 0.5Hz pwm, 50% Duty Cycle
			motorDrive(0.2,0.75)		# 0.2Hz pwm, 75% Duty Cycle
	except KeyboardInterrupt:
		print("Process terminated by user")
	finally:
		GPIO.cleanup()  # Reset GPIO pins to default

