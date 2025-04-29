import numpy as np
import tensorflow as tf
from guizero import App, Box, Picture, Text, PushButton
import cv2
import subprocess
from io import BytesIO
from tkinter import PhotoImage
from PIL import Image
import time
import os

# Load TensorFlow Lite model
interpreter = tf.lite.Interpreter(model_path="model_unquant.tflite")
interpreter.allocate_tensors()

# Directory to OS
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))

# Get model input and output details
input_details  = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Mapping of gesture predictions based on label.txt file
GESTURE_MAP = {
    1: "Peace Sign",
    0: "No Peace Sign",
}

# Turn photo to an array
def preprocess_image(frame):
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224, 224))
    image = np.array(image, dtype=np.float32) / 255.0
    return np.expand_dims(image, axis=0)

# Utilizing preprocess image to return the appropiate gesture
def predict_gesture(frame):
    img = preprocess_image(frame)
    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()
    probs = interpreter.get_tensor(output_details[0]['index'])[0]
    idx   = np.argmax(probs)
    return GESTURE_MAP.get(idx, "Unknown"), float(probs[idx])

# GUI
app = App("Hand Capture", width=640, height=480)
box                = Box(app, width="fill", height="fill")
camera_picture     = Picture(box, width=320, height=240)
result_text        = Text(app, text="Make your gesture!", size=20)
pi_gesture_display = Text(app, text="", size=18)
play_button        = PushButton(app, text="Start", width=10, height=2)

# Allow program to communicate with camera
def capture_image():
    subprocess.run([
        "libcamera-still", "--output", "frame.jpg",
        "--width", "640", "--height", "480",
        "--timeout", "1", "--nopreview"
    ], check=True)
    frame = cv2.imread("frame.jpg")
    if frame is not None:
        frame = cv2.rotate(frame, cv2.ROTATE_180)
    return frame

# Refreshing the camera frames
def update_camera_feed():
    frame = capture_image()
    if frame is not None:
        frame = cv2.flip(frame, 1)
        rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        small = cv2.resize(rgb, (320, 240))
        bio   = BytesIO()
        Image.fromarray(small).save(bio, format="PNG")
        bio.seek(0)
        photo = PhotoImage(data=bio.read())
        camera_picture.image = photo
        camera_picture.tk.update()
    app.after(10, update_camera_feed)

# Ensure there is a camera output and capture the frame based on confidence of gesture
def detect_loop():
    frame = capture_image()
    if frame is None:
        result_text.value = "Camera error!"
        play_button.enable()
        return

    gesture, confidence = predict_gesture(frame)
    result_text.value        = f"Gesture: {gesture}"
    pi_gesture_display.value = f"Confidence: {confidence:.2f}"

    if gesture == "Peace Sign" and confidence > 0.99:
        # capture and stop looping
        photos_dir = os.path.join(BASE_DIR, "photos")
        os.makedirs(photos_dir, exist_ok=True)
        fname = os.path.join(photos_dir, f"photo_{int(time.time())}.jpg")
        cv2.imwrite(fname, frame)
        result_text.value += "\nCaptured!"
        print(f"📸 Saved {fname}")
        play_button.enable()
    else:
        # keep looking every 1000 ms to allow hand to enter frame
        app.after(1000, detect_loop)

# Start button
def start_game():
    # disable button to prevent re-entry
    play_button.disable()
    result_text.value        = "Detecting..."
    pi_gesture_display.value = ""
    detect_loop()

play_button.update_command(start_game)

# Continuous camera preview
update_camera_feed()
app.display()
