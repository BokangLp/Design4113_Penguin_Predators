import time
import RPi.GPIO as GPIO

# Drive the speakers using specified frequency(Hz) and duty cycle (as a decimal)
def speakerDrive(frequency,DutyCycle,speaker_Pin):
	
	pwm_13 = GPIO.PWM(speaker_Pin,frequency)	# Set GPIO13 to PWM
	pwm_13.start(DutyCycle)
	return pwm_13

def ledDrive(frequency,DutyCycle,LED_Pin):
	pwm_12 = GPIO.PWM(LED_Pin,frequency)
	pwm_12.start(DutyCycle)
	return pwm_12

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

