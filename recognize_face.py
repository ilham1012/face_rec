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
# video_capture = cv2.VideoCapture("rtsp://admin:microsoftiit@192.168.21.68:8080")

# Load classifier model

clf = joblib.load('SVM-test.pkl') 

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []

odd_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if odd_frame:
        # Find all the faces and face encodings in the current frame of video
        
        time_0 = time.time()
        face_locations = face_recognition.face_locations(rgb_frame)
        time_1 = time.time()

        print(len(face_locations), " face(s) on: ", time_1 - time_0, "s")

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
            print("Name: ", name)
            print("Prob: ", max_prob)
            print("lmrk: ", time_3 - time_2, ", enc: ", time_4 - time_3, ", pred: ", time_5 - time_4)

            if max_prob > THRESHOLD:
                # OPEN THE DOOR
                print("OPEN THE DOOR")

            print("-----")
       
    odd_frame = not odd_frame

    
    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
