# Import necessary libraries
import face_recognition  # Face recognition library
import cv2  # OpenCV for video capture and processing
from time import sleep  # Sleep function for waiting

# Load allowed user images and encode them
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

# Loop through allowed_users dictionary, load images, and calculate face encodings
for name, image_files in allowed_users.items():
    for image_file in image_files:
        image = face_recognition.load_image_file(image_file)  # Load image file
        face_encodings_list = face_recognition.face_encodings(image)  # Calculate face encodings

        if not face_encodings_list:  # Check if the list is empty
            print(f"No face detected in {image_file}")
            continue

        face_encoding = face_encodings_list[0]
        known_face_encodings.append(face_encoding)  # Add the face encoding to the list
        known_face_names.append(name)  # Add the user name to the list

# Initialize the camera
try:
    video_capture = cv2.VideoCapture(0)  # Open the camera for video capture
except Exception as e:
    print(f"Error: Unable to open camera. {str(e)}")
    exit()

if not video_capture.isOpened():
    print("Error: Unable to open camera.")
    exit()
# The rest of the code remains the same

# Main loop for video processing and face recognition
while True:
    ret, frame = video_capture.read()  # Read a frame from the video capture
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)  # Resize the frame to 1/4 size for faster processing
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB).astype("uint8")  # Convert the frame from BGR to RGB (face_recognition uses RGB)


    # Detect face locations and calculate face encodings for the current frame
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    # Loop through detected face encodings
    for face_encoding in face_encodings:
        # Compare the current face encoding with known face encodings
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"  # Set the default name as "Unknown"

        # Check if any known face encoding matches the current face encoding
        if True in matches:
            first_match_index = matches.index(True)  # Get the index of the first match
            name = known_face_names[first_match_index]  # Get the name of the matched user


            print(f"Simulated access granted for {name}")  # Print the name of the granted user
            sleep(5)  # Wait for 1 second

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the video capture and close all windows
video_capture.release()  # Release the video capture object
cv2.destroyAllWindows()  # Close all OpenCV windows
