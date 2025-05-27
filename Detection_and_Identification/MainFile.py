# Import libraries
import time
from picamera2 import Picamera2
import io
import cv2
import os
import RPi.GPIO as GPIO
import asyncio
import random


# Import helper functions
import DetectAndCapture
import DeterrenceCode
#import Classify
import SendDetectionData

#Initialize GPIO
input_pin = 24
LED_pin = 12
motor_pin = 6
speaker_pin = 13
GPIO.setmode(GPIO.BCM) # Use the GPIO labels instead of board labels
GPIO.setup(input_pin, GPIO.IN)
GPIO.setup(LED_pin,GPIO.OUT)
GPIO.setup(speaker_pin, GPIO.OUT)
GPIO.setup(motor_pin, GPIO.OUT)

#Main function
async def main():
	# Initial responses
	response = [[500,40],[200,60],[50,80]]
	image = None
	timestamp = None
	img_class = ""
	Led_response = []
	speaker_respone = []
	duration = 0
	img_class = "Badger"

	# Initialize camera
	picam2 = DetectAndCapture.initCam()
	while True:
		try:
			pin_status = GPIO.input(input_pin)
			while not(pin_status):	# Wait for motion to be detected
				pin_status = GPIO.input(input_pin)
			print("Motion Sensed! Capturing Image!") 
			timestamp = time.localtime()
			if int(time.strftime("%H", timestamp)) >= 18 or int(time.strftime("%H",timestamp))<=6:
				GPIO.output(LED_pin, GPIO.HIGH)
			image,image_name = await DetectAndCapture.capture_and_save(picam2)
			await asyncio.sleep(0.5)
			#await Classify.preprocess_image(image)
			#imag_class = await Classify.classify_image(image)

			if img_class == "Badger":
				startTime = time.time()
				if int(time.strftime("%H", timestamp)) >= 18 or int(time.strftime("%H",timestamp))<=6:
					Led_response = response[random.randint(0,10)%3]
				speaker_response = response[random.randint(0,10)%3]
				pwm_12 = DeterrenceCode.ledDrive(Led_response[0],Led_response[1],LED_pin)
				pwm_13 = DeterrenceCode.speakerDrive(speaker_response[0],speaker_response[1],speaker_pin)
				DeterrenceCode.motorDrive(motor_pin)
				while pin_status:
					pin_status = GPIO.input(input_pin)
				time.sleep(10)
				endTime = time.time()
				pwm_13.stop()
				pwm_12.stop()
				GPIO.output(motor_pin,GPIO.LOW)
				duration = endTime - startTime
			deterrence = {"LED": Led_response,
				"Speaker": speaker_response,
				"motor": "ON"}
			await SendDetectionData.send_detection_data(image,image_name,deterrence,duration)
		except KeyboardInterrupt:
			print("Program stopped by server")
			break
		except Excpetion as e:
			print("Program interrupted: {e}")
		finally :
			print("Connection closed.")


if __name__ == "__main__":
	asyncio.run(main())
