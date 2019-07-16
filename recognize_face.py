import face_recognition
import cv2
import numpy as np
from sklearn.externals import joblib
import time

# Const
# Threshold for face recognition confidence score
# If the confidence > threshold, open the door
THRESHOLD = 0.85


# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
# video_capture = cv2.VideoCapture("http://admin:iit19@192.168.236.250:8080/stream/video/mjpeg")

# Load classifier model

clf = joblib.load('models/ada__2019-07-16_14-11-06.pkl')

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []

RESIZE_FACTOR = 4
FRAME_SKIPPING = 10

frame_idx = 0
odd_frame = True

def recognize_face(rgb_frame):
    # Find all the faces and face encodings in the current frame of video
    time_0 = time.time()
    face_locations = face_recognition.face_locations(rgb_frame)
    time_1 = time.time()

    # print(len(face_locations), " face(s) on: ", time_1 - time_0, "s")

    if (len(face_locations) == 1):

        time_2 = time.time()
        faces_landmarks = face_recognition.face_landmarks(rgb_frame, face_locations)
        time_3 = time.time()
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        time_4 = time.time()
        
        prob = clf.predict_proba(face_encodings)
        time_5 = time.time()

        max_prob_idx = prob.argmax(axis=1)
        name = clf.classes_[max_prob_idx][0]
        max_prob = prob[0][max_prob_idx][0]
        
        print("-----")
        print("Name: ", name, " ", max_prob)
        print("Total Time: ", time_5 - time_0)
        # print("lmrk: ", time_3 - time_2, ", enc: ", time_4 - time_3, ", pred: ", time_5 - time_4)

        if max_prob > THRESHOLD:
            # OPEN THE DOOR
            print("OPEN THE DOOR")

        print("-----")


while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/2 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=1/RESIZE_FACTOR, fy=1/RESIZE_FACTOR)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    # if odd_frame:
    if frame_idx == FRAME_SKIPPING:
        print("process!")
        frame_idx = 0
        recognize_face(rgb_frame)
    # odd_frame = not odd_frame
    else:
        frame_idx += 1
        
    print("idx: ", frame_idx)

    
    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
