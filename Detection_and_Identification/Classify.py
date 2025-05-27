# Classification libraries
import numpy as np
import tensorflow as tf
from PIL import Image

# Load and preprocess the image
async def preprocess_image(image, target_size=(128, 128)): # OR use image path (import os firstly)
    img = Image.open(image).convert('RGB')
    img = img.resize(target_size)
    img_array = np.array(img).astype(np.float32) / 255.0  # Normalize to [0, 1]
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array

# Inference function
async def classify_image(image): # or use imagepath
    # Load the TFLite model and allocate tensors
    interpreter = tf.lite.Interpreter(model_path="Penguin_Badger.tflite")
    interpreter.allocate_tensors()

    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Clasiffy image
    input_data = preprocess_image(image)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    predicted_class = np.argmax(output_data)
    confidence = np.max(output_data)

    class_labels = ['Badger','Penguin']  #Two classes
    return class_labels[predicted_class]

