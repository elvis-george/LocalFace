import face_recognition  # Import the face_recognition library
import cv2  # Import the OpenCV library for video processing
from picamera.array import PiRGBArray  # Import PiRGBArray to capture images as NumPy arrays
from picamera import PiCamera  # Import PiCamera to interact with the Raspberry Pi camera
import numpy as np  # Import NumPy to work with arrays
# import RPi.GPIO as GPIO  # Import the RPi.GPIO library to control the Raspberry Pi's GPIO pins (Not needed for testing)
from time import sleep  # Import sleep from the time module to pause the program

# relay_pin = [26]  # Define the GPIO pin number (BCM mode) for the relay (Not needed for testing)
# GPIO.setmode(GPIO.BCM)  # Set the GPIO pin numbering mode to BCM mode (Not needed for testing)
# GPIO.setup(relay_pin, GPIO.OUT)  # Set the relay_pin as an output pin (Not needed for testing)
# GPIO.output(relay_pin, 0)  # Set the initial output of the relay_pin to 0 (off) (Not needed for testing)

# Load allowed user images and calculate face encodings (same as the previous Mac version)
allowed_users = {
    "user1": [
        "/Users/localhost/ElvisDetect/elvisDetect/user1.jpg",
        "/Users/localhost/ElvisDetect/elvisDetect/user2.jpg",
        "/Users/localhost/ElvisDetect/elvisDetect/user3.jpg",
        "/Users/localhost/ElvisDetect/elvisDetect/user4.jpg"
    ]
}

known_face_encodings = []  # List to store the face encodings of allowed users
known_face_names = []  # List to store the names of allowed users
camera = PiCamera()  # Create a PiCamera object to interact with the Raspberry Pi camera
camera.resolution = (640, 480)  # Set the camera resolution to 640x480 pixels
camera.framerate = 30  # Set the camera frame rate to 30 frames per second
rawCapture = PiRGBArray(camera, size=(640, 480))  # Create a PiRGBArray object to store frames as NumPy arrays

# Start an infinite loop that captures video frames continuously
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = frame.array  # Convert the captured frame from PiRGBArray to a NumPy array
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)  # Resize the frame to 1/4 size for faster processing
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)  # Convert the frame color space from BGR to RGB

    # Detect face locations and calculate face encodings
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    # Loop through detected face encodings
    for face_encoding in face_encodings:
        # Compare the current face encoding with known face encodings
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"  # Set the default name as "Unknown"

        # If any known face encoding matches the current face encoding, get the name of the matched user
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

            print(f"Simulated access granted for {name}")  # Print the name of the granted user
            # GPIO.output(relay_pin, 1)  # Set the relay_pin output to 1 (on) (Not needed for testing)
            sleep(1)  # Wait for 1 second
        else:
            print("Access denied")  # Print "Access denied" if no match is found
            # GPIO.output(relay_pin, 0)  # Set the relay_pin output to 0 (
            # off) (Not needed for testing)

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    # Release the video capture and close all windows
    rawCapture.truncate(0)  # Clear the rawCapture buffer for the next frame

cv2.destroyAllWindows()  # Close all the windows
