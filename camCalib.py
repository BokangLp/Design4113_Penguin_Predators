import socket
import os
import json
import time
import cv2
from picamera2 import Picamera2
import base64

# Initialize cam
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration(main={"size":(1800,1624)}))
picam2.start()
print("Cam initialized successfully")
time.sleep(5)


import socket
import os
import json
import base64

def capture_Image(brightness,saturation,contrast):
	try:	
		# Capture image
		print("Capturing image...")
		image = picam2.capture_array()
		print("Image captured!")

		# Convert image color to BGR
		image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

		# Save the image immediately after conversion
		filename = "Image"+str(brightness)+str(saturation)+str(contrast)+".jpg"
		return(image,filename)
	
	except Exception as e:
		print(f"Error during sending of data: {e}")

def send_image(image, image_name,server_ip, port):
    # Encode image to base64
    image_base64 = base64.b64encode(image).decode('utf-8')

    # Create JSON-compatible dictionary
    data = {
        "image_name": image_name,
        "image": image_base64
    }

    # Serialize to JSON
    json_data = json.dumps(data).encode('utf-8')
    data_size = len(json_data)

    # Connect to server and send data
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, port))
    try:
        # Send the size of JSON data (4 bytes, big-endian)
        sock.sendall(data_size.to_bytes(4, 'big'))
        # Send the actual JSON data
        sock.sendall(json_data)
        print(f"Sent image '{data['image_name']}' ({data_size} bytes)")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()
        time.sleep(5)

# Example usage
if __name__ == "__main__":
    print("Initializing cam")
    picam2 = Picamera2()
    picam2.configure(picam2.create_still_configuration(main={"size":(1800,1624)}))
    picam2.start()
    print("Cam initialized successfully")

    SERVER_IP = "192.168.137.1"  # Use the actual IP of the receiver
    PORT = 5555
    
    try:
        for j in range(21):
            for k in range(21):
                 for l in range(21):
                      controls = {"AeEnbale":True,
                                  "AwbEnable": True,
                                "Brightness":(j/10)-1,
                                "Saturation":(k/10),
                                "Contrast":l/10,
                      }
                      picam2.set_controls(controls)
                      image,image_name = capture_Image((j/10 -1),k/10,l/10)
                      send_image(image,image_name,SERVER_IP,PORT)
    except KeyboardInterrupt:
         print("Connection interrupted by user.")
    finally:
         print("Connection closed")
