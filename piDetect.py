import face_recognition
import cv2
import numpy as np
import time
from time import sleep
import wiringpi

lockState = 'locked'
wiringpi.wiringPiSetup()
wiringpi.pinMode(0, 1)
wiringpi.pinMode(2, 1)
wiringpi.pinMode(3, 1)
wiringpi.digitalWrite(0, 1)

def unlock():
    global lockState
    if lockState == 'unlocked':
        print('ERROR: already unlocked!')
        return False
    else:
        t_end = time.time() + 2.5
        while time.time() < t_end:
            wiringpi.digitalWrite(2, 1)

        wiringpi.digitalWrite(2, 0)
        lockState = 'unlocked'
        return True

def lock():
    global lockState
    if lockState == 'locked':
        print('ERROR: already locked!')
        return False
    else:
        t_end = time.time() + 2.5
        while time.time() < t_end:
            wiringpi.digitalWrite(3, 1)

        wiringpi.digitalWrite(3, 0)
        lockState = 'locked'
        return True
#add users and images
allowed_users = {
    "user1": [
        "/home/localhost/elvisDetect/valid_photoID/user1.jpg",
        "/home/localhost/elvisDetect/valid_photoID/user2.jpg",
        "/home/localhost/elvisDetect/valid_photoID/user3.jpg",
        "/home/localhost/elvisDetect/valid_photoID/user4.jpg"
    ]
}

known_face_encodings = []
known_face_names = []

# Replace this line with the index of your USB camera, usually 0 or 1
camera = cv2.VideoCapture(0)

# Loop through allowed_users dictionary, load images, and calculate face encodings
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

# Start an infinite loop that captures video frames continuously
while True:
    ret, frame = camera.read()

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
            unlock()
            sleep(5)

        else:
            print("Access denied")
            lock()
            sleep(1)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
