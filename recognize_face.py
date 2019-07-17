import time
import argparse

import face_recognition
import cv2
import numpy as np
from sklearn.externals import joblib

from utils import constant

import pandas as pd

# Const
# Threshold for face recognition confidence score
# If the confidence > threshold, open the door
THRESHOLD = 0.85



# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument(
    "-m", "--model",
    default="svm",
    help="choose in ['dt', 'svm', 'rf', 'adaboost']"
    )
ap.add_argument(
    "-v", "--video_capture",
    default="ip_cam",
    help="choose ['0', '1', 'ip_cam']"
    )
ap.add_argument(
    "-n", "--n_test",
    default=100,
    help="location of test file"
    )
args = vars(ap.parse_args())


# Get a reference to webcam #0 (the default one)
video_capture = None

time_x = time.time()
if (args['video_capture'] == '0'):
	video_capture = cv2.VideoCapture(0)
elif (args['video_capture'] == '1'):
	video_capture = cv2.VideoCapture(1)
else:
	video_capture = cv2.VideoCapture("http://admin:admin@192.168.0.10:8080/stream/video/mjpeg")
print("vc took ", time.time() - time_x, "s")

# Load classifier model

if (args['model'] == constant.MODELS[0]): #dt
	clf = joblib.load('models/dt__2019-07-16_14-08-52.pkl')
elif (args['model'] == constant.MODELS[1]): #svm
        clf = joblib.load('models/svm__2019-07-16_14-09-42.pkl')
elif (args['model'] == constant.MODELS[3]): #rf
        clf = joblib.load('models/rf__2019-07-16_14-10-34.pkl')
else:
        clf = joblib.load('models/ada__2019-07-16_14-11-06.pkl')


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []

RESIZE_FACTOR = 4
FRAME_SKIPPING = 10

frame_idx = 0
odd_frame = True

# FOR TESTING ONLY
N_TESTING = args['n_test']
det_times = []
lmk_times = []
enc_times = []
clf_times = []

def recognize_face(rgb_frame):
    # Find all the faces and face encodings in the current frame of video
    time_0 = time.time()
    face_locations = face_recognition.face_locations(rgb_frame, model="hog")
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

        if (name != "unknown") and (max_prob > THRESHOLD):
            # OPEN THE DOOR
            print("OPEN THE DOOR")

        print("-----")

        det_times.append(time_1 - time_0)
        lmk_times.append(time_3 - time_2)
        enc_times.append(time_4 - time_3)
        clf_times.append(time_5 - time_4)

    


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
        # print("process!")
        frame_idx = 0
        recognize_face(rgb_frame)
    # odd_frame = not odd_frame
    else:
        frame_idx += 1
        
    # print("idx: ", frame_idx)

    
    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # FOR TESTING
    if len(clf_times) > N_TESTING + 10:
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()


# FOR TESTING
df = pd.DataFrame(list(zip(det_times, lmk_times, enc_times, clf_times)),
                    columns=['Face Detection', 'Finding Landmarks', 'Face Encoding', 'Classification'])

print(df)
output_name = 'experiments/running_test__' + args['model'] + '.csv'
df.to_csv(output_name)
