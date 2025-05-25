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

pin_num = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_num, GPIO.IN)

#Initializing cam
print("Initializing cam")
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration(main={"size":(1800,1624)}))
picam2.start()
print("Cam initialized successfully")

time.sleep(5)

# Update camera settings
controls = {"AeEnable": True,
	"Brightness":0.2,	# -1.0 -> 1.0
	"Contrast":1.0,		# 0.0 -> 2.0
	"Saturation":1.0	# 0.0 -> 2.0
}
picam2.set_controls(controls)
picam2.set_controls({"AwbEnable": True})	# Enable auto white balance

# Link of websocket
WS_URI = "ws://192.168.137.1:5557"

# Capture and send image data
async def capture_and_send():
	# Connect to websocket
	try:
		async with websockets.connect(WS_URI) as websocket:
			print("Websocket connected")
	except Exception as e:
		print("Connection failed")
	# Main loop
	while True:
		try:	
			# Capture image
			print("Capturing image...")
			image = picam2.capture_array()
			print("Image captured!")
			local_time = time.localtime()		# Get current local time

			# Convert image color to BGR
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
			print("Data serialized successfullyy")			

			# Send data to the server
			await websocket.send(json_data)
			print("Data sent!")
			await asyncio.sleep(5)
	
		except Exception as e:
			print(f"Error during capture and send: {e}")
			await asyncio.sleep(1)
#Main function
async def main():
	try:
		pin_status = GPIO.input(pin_num)
		while not(pin_status):	# Wait for motion to be detected
			pin_status = GPIO.input(pin_num)
		print("Motion Sensed! Capturing Image!") 
		await capture_and_send()
		await asyncio.sleep(1)
	except KeyboardInterrupt:
		print("Capture loop interrupted")
	finally :
		GPIO.cleanup()
		print("Connection closed.")


if __name__ == "__main__":
	asyncio.run(main())
