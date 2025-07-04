import socket
import time
from picamera2 import Picamera2
import io
import cv2
import os
import RPi.GPIO as GPIO
import base64
import json

pin_num = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_num, GPIO.IN)

#Initializing cam
print("Initializing cam")
picam2 = Picamera2()
#picam2.resolution = (2592, 1944)	# Maximize pixels
picam2.configure(picam2.create_still_configuration(main={"size":(1800,1624)}))
picam2.start()
print("Cam initialized successfully")

time.sleep(5)

# Update camera settings
controls = {"AeEnable": True,
		#"ExposureTime": 50000,
	#"AnalogueGain": 5.0
	"Brightness":0.2,	# -1.0 -> 1.0
	"Contrast":1.0,		# 0.0 -> 2.0
	"Saturation":1.0	# 0.0 -> 2.0
}
picam2.set_controls(controls)
picam2.set_controls({"AwbEnable": True})	# Enable auto white balance

# Connect to pc
HOST = '192.168.137.1'
PORT = 5557

# Create and connect socket
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.connect((HOST,PORT))

# Capture and send image
def capture_and_send():
	# Create and connect socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((HOST,PORT))

	# Capture image
	try:	
		print("Capturing image...")
		image = picam2.capture_array()
		print("Image captured!")
		local_time = time.localtime()		# Get current local time
	except Exception as e:
		print(f"Camera capture failed: {e}")
	
	# Convert image color toBGR
	image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
	
	# Convert image to bytes
	success, encode_image = cv2.imencode('.jpg',image,[int(cv2.IMWRITE_JPEG_QUALITY),95])
	if not success:
		print("Failed to encode image")
		return
	image_bytes = base64.b64encode(encode_image.tobytes()).decode('utf-8')
	print("Image successfully encode as JPEG")
	
	# Data sent to the server
	data =  {
		"timeStamp": time.strftime("%Y-%m-%d %H:%M:%S",local_time),
		"image_size": len(encode_image),
		"image": image_bytes  
	}

	# Serialize the data
	json_data = json.dumps(data).encode('utf-8')
	
	# Send data to the server
	sock.sendall(json_data)
	print("Data sent!")

# Execute capture and send
num_files = 0
try:
	while True:
		#pin_status = GPIO.input(pin_num)
		#if pin_num:
		print("Motion Sensed! Turning Cam on!") 
		capture_and_send()
		num_files+=1
		#else:
		#	print("Still safe! No motion")
		#	continue
		time.sleep(5)
except KeyboardInterrupt:
	print("Capture loop interrupted")
finally :
	#sock.close()
	GPIO.cleanup()
	print("Connection closed.")
	print(f"Number of files send : {num_files}. ")

