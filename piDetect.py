import face_recognition
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import RPi.GPIO as GPIO
from time import sleep

relay_pin = [26]
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)
GPIO.output(relay_pin, 0)

# Load allowed user images and encode them
# Replace these paths with the paths to the allowed user images on your Raspberry Pi
allowed_users = {
    "user1": [
        "/path/to/user1.jpg",
        "/path/to/user2.jpg",
        "/path/to/user3.jpg",
        "/path/to/user4.jpg"
    ]
}

known_face_encodings = []
known_face_names = []

for name, image_files in allowed_users.items():
    for image_file in image_files:
        image = face_recognition.load_image_file(image_file)
        face_encodings_list = face_recognition.face_encodings(image)

        if not face_encodings_list:
            print(f"No face detected in {image_file}")
            continue

        face_encoding = face_encodings_list[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(name)

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = frame.array
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

            print(f"Simulated access granted for {name}")
            GPIO.output(relay_pin, 1)
            sleep(1)
        else:
            GPIO.output(relay_pin, 0)

    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)

    rawCapture.truncate(0)

    if key == 27:
        break

cv2.destroyAllWindows()
