import socket
import base64
import json
import asyncio
import cv2
import time
import traceback

# Data sending function
async def send_detection_data(image,image_name):
	# Socket information
	server_ip = "192.168.137.1"
	port = 5555
	try:
		# Connect websocket
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((server_ip,port))
	
        	# Convert image to bytes
		success, encode_image = cv2.imencode('.jpg',image,[int(cv2.IMWRITE_JPEG_QUALITY),95])
		if not success:
			print("Failed to encode image")
			return
		image_bytes = base64.b64encode(encode_image.tobytes()).decode('utf-8')
		print("Image successfully encoded as JPEG")
	
		# Data sent to the server
		data =  {
			"image_name": image_name,
			"image": image_bytes  
		}

		# Serialize the data
		json_data = json.dumps(data).encode('utf-8')
		data_size = len(json_data)
		print("Data serialized successfully")			

		# Send data to the server
		sock.sendall(data_size.to_bytes(4,'big'))
		sock.sendall(json_data)
		print("Data sent!")
	
	except Exception as e:
		print(f"Error during sending of data: {e}")
		traceback.print_exc()
		await asyncio.sleep(1)

async def main():
	import DetectAndCapture
	try:
		picam2 = DetectAndCapture.initCam()
		image,image_name = await DetectAndCapture.capture_and_save(picam2)
		await send_detection_data(image,image_name)
	except Exception as e:
		print(f"Exception: {e}")

if __name__ == "__main__":
	asyncio.run(main())
