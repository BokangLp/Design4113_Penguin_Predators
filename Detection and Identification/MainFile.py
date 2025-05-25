# Import libraries
import websockets
import time
from picamera2 import Picamera2
import io
import cv2
import os
import RPi.GPIO as GPIO
import base64
import json
import asyncio
import random

# Classification libraries
import numpy as np
import tensorflow as tf
from PIL import Image
import os

# Import helper functions
import DetectAndCapture
import DeterrenceCode
import Classify
import SendDetectionData

#Initialize GPIO
input_pin = 24
LED_pin = 12
motor_pin = 6
speaker_pin = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(input_pin, GPIO.IN)
GPIO.setup(LED_pin,GPIO.OUT)
GPIO.setup(speaker_pin, GPIO.OUT)
GPIO.setup(motor_pin, GPIO.OUT)

# Initial responses
response = [[17000,0.5],[26000,0.5],[22000,0.5]]

#Main function
async def main():
    image = None
    timestamp = None
    img_class = ""
    Led_response = []
    speaker_respone = []
    duration = 0

    # Initialize camera
    DetectAndCapture.initCam()
    while True:
        try:
            pin_status = GPIO.input(input_pin)
            while not(pin_status):	# Wait for motion to be detected
                pin_status = GPIO.input(input_pin)
            print("Motion Sensed! Capturing Image!") 
            timestamp = time.localtime()
            if int(time.strftime("%H", timestamp)) >= 18 or int(time.strftime("%H",timestamp))<=6:
                 GPIO.output(LED_pin, GPIO.HIGH)
            await image = DetectAndCapture.capture_and_save()
            await asyncio.sleep(1)
            await Classify.preprocess_image(image)
            await imag_class = Classify.classify_image(image)

            if img_class == ("Badger"):
                startTime = time.time()
                if int(time.strftime("%H", timestamp)) >= 18 or int(time.strftime("%H",timestamp))<=6:
                    Led_response = response[random(10)//3]
                speaker_response = response[random(10)//3]
                DeterrenceCode.ledDrive(Led_response,LED_pin)
                DeterrenceCode.speakerDrive(speaker_response,speaker_pin)
                DeterrenceCode.motorDrive(motor_pin)
                while pin_status:
                     pin_status = GPIO.input(input_pin)
                endTime = time.time()
                GPIO.output(LED_pin,GPIO.LOW)
                GPIO.output(speaker_pin,GPIO.LOW)
                GPIO.output(motor_pin,GPIO.LOW)
                duration = endTime - startTime
            duration = duration/1000        # Convert duration to seconds
            deterrence = {"LED": Led_response,
                          "Speaker": speaker_response}
            
            SendDetectionData.send_detection_data(image,timestamp,deterrence, duration)
        except KeyboardInterrupt:
            print("Capture loop interrupted")
        finally :
            GPIO.cleanup()
            print("Connection closed.")


if __name__ == "__main__":
	asyncio.run(main())