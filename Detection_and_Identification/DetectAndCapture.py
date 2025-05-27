import websockets
import time
from picamera2 import Picamera2
import io
import cv2
import os
import base64
import json
import asyncio

# Initializing cam
def initCam():
	print("Initializing cam")
	picam2 = Picamera2()
	picam2.configure(picam2.create_still_configuration(main={"size":(1800,1624)}))
	picam2.start()
	print("Cam initialized successfully")

	time.sleep(5)

	# Update camera settings
	picam2.set_controls({"AwbEnable": True})	# Enable auto white balance
	return(picam2)

# Capture and send image data
async def capture_and_save(picam2):
	try:	
		# Capture image
		print("Capturing image...")
		image = picam2.capture_array()
		print("Image captured!")
		local_time = time.localtime()		# Get current local time

		# Convert image color to BGR
		image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

		# Save the image immediately after conversion
		filename = time.strftime("Image_%Y%m%d_%H%M%S.jpg", local_time)
		cv2.imwrite(filename, image)
		return(image,filename)
	
	except Exception as e:
		print(f"Error when capturing and saving image: {e}")
		await asyncio.sleep(1)


async def main():
	try:
		picam2 = initCam()
		log_time = time.localtime()
		image_name = await capture_and_save(picam2)
		print(f"Image saved as {image_name}")
	except Exception as e:
		print(f"Excption: {e}")

if __name__ == "__main__":
	asyncio.run(main())
