import websockets
import base64
import json
import asyncio
import cv2
import time


# Data sending function
async def send_detection_data(image,timestamp,deterrence):
	# Link of websocket
	WS_URI = "ws://192.168.137.1:5557"
	# Connect to websocket
	try:
		async with websockets.connect(WS_URI) as websocket:
			print("Websocket connected")
	except Exception as e:
		print("Connection failed")
		await asyncio.sleep(1)
	try:
        # Convert image to bytes
		success, encode_image = cv2.imencode('.jpg',image,[int(cv2.IMWRITE_JPEG_QUALITY),95])
		if not success:
			print("Failed to encode image")
			return
		image_bytes = base64.b64encode(encode_image.tobytes()).decode('utf-8')
		print("Image successfully encode as JPEG")
	
		# Data sent to the server
		data =  {
			"timeStamp": time.strftime("%Y-%m-%d %H:%M:%S",timestamp),
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
		print(f"Error during sending of data: {e}")
		await asyncio.sleep(1)