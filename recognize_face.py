import time
import sys
import argparse

import face_recognition
import cv2
import numpy as np
from sklearn.externals import joblib
#from firebase import firebase

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
faces_landmarks = []
face_names = []

RESIZE_FACTOR = 4
FRAME_SKIPPING = 10

frame_idx = 0
odd_frame = True

device_url = '/gedung30/lab_iit/pintu'


# FOR TESTING ONLY
N_TESTING = args['n_test']
det_times = []
lmk_times = []
enc_times = []
clf_times = []
just_open = False
justcount = 0



def relock(response):
    print(response)
    time.sleep(2)
    # result = firebase.put(device_url, 'lock', True)
    # print(result)


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
            just_open = True
            # result = firebase.put_async(device_url, 'lock', False, callback=relock)
            # result = firebase.put(device_url, 'lock', False)
            # relock(result)
            return face_locations, just_open, faces_landmarks

        print("-----")
        return [], False, faces_landmarks


        # det_times.append(time_1 - time_0)
        # lmk_times.append(time_3 - time_2)
        # enc_times.append(time_4 - time_3)
        # clf_times.append(time_5 - time_4)

    return [], False, []
    

def my_filled_circle(img, center):
    center = tuple([RESIZE_FACTOR * x for x in center])
    cv2.circle(img, center, 2, (255, 200, 255))


# firebase = firebase.FirebaseApplication('https://lab-iit.firebaseio.com', None)
# doorlock = firebase.get(device_url, None)
# print("FIREBASE : ", doorlock)

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/2 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=1/RESIZE_FACTOR, fy=1/RESIZE_FACTOR)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = small_frame[:, :, ::-1]


    # DEMO
    if (just_open):
        # Pause processing for 300 frame
        # print("just_count: ", justcount)
        justcount += 1

        if (justcount > 100):
            justcount = 0
            just_open = False
        
    else:
        # Only process every other frame of video to save time
        # if odd_frame:
        if frame_idx == FRAME_SKIPPING:
            # print("process!")
            frame_idx = 0
            face_locations, just_open, faces_landmarks = recognize_face(rgb_frame)
        # odd_frame = not odd_frame
        else:
            frame_idx += 1
        
    # print("idx: ", frame_idx)

    # Display the results
    for top, right, bottom, left in face_locations:
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    for face_landmarks in faces_landmarks:
        for landmark in face_landmarks:
            # print(landmark)
            for point in face_landmarks[landmark]:
                my_filled_circle(frame, point)
    
    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # Release handle to the webcam
        print('===== Q =====')
        cv2.destroyAllWindows()
        print('===== Destroy Windows =====')
        break

print('===== VC Release =====')
# video_capture.release()
print("close")
sys.exit()
