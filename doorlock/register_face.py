import time

import cv2
import numpy as np
import face_recognition
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, auc, cohen_kappa_score, f1_score, precision_score, recall_score
import joblib
import hashlib

from utils import constant, util
from doorlock.constants import DATASET_URL, MODEL_URL

class RegisterFace():
    NEW_DATA = 125
    ACC_THRESHOLD = .95

    prev_train_dataset = None
    new_train_dataset = None
    prev_test_dataset = None
    new_test_dataset = None
    
    username = None
    face_encodings = []

    def __init__(self, users_df):
        self.prev_train_dataset = util.load_data(DATASET_URL + 'face_encodings__train_.csv')
        self.prev_test_dataset = util.load_data(DATASET_URL + 'face_encodings__test_.csv')
        self.users_df = users_df

    def set_data(self, user):
        self.user_df = user
        self.username = user.username.item()
        print(self.username)
    
    def capture_face(self, rgb_frame, model="hog"):
        print("recorded: " , len(self.face_encodings))
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame, model=model)
        
        # Make sure there is ONE face detected
        if (len(face_locations) == 1):
            face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
            self.face_encodings.append(face_encoding)

    def data_prep(self):
        ret = False

        # Create Dataframe from Face Encodings
        df = pd.DataFrame(self.face_encodings, columns=[str(col) for col in range(128)])
        # Add username to Dataframe
        df['128'] = self.username
        # Split Train Test
        self.new_train_dataset, self.new_test_dataset = train_test_split(df, test_size=0.2)
        # Merge prev dataset with new dataset
        self.new_train_dataset = pd.concat([self.prev_train_dataset, self.new_train_dataset])
        self.new_test_dataset = pd.concat([self.prev_test_dataset, self.new_test_dataset])
        # Split Feature and Label for training
        X_train, X_test, y_train, y_test = util.split_xy_train_test(self.new_train_dataset, self.new_test_dataset)
        # Train model with new data
        clf, acc_score = self.train_new_data(X_train, X_test, y_train, y_test)

        if (acc_score > self.ACC_THRESHOLD):
            # Save new datasets (overwrite)
            self.new_train_dataset.to_csv(DATASET_URL + 'face_encodings__train_.csv_', index=False)
            self.new_test_dataset.to_csv(DATASET_URL + 'face_encodings__test_.csv_', index=False)
            # Save model (overwrite)
            joblib.dump(clf, MODEL_URL + 'model_.pkl')
            self.users_df = pd.concat([self.users_df, self.user_df], ignore_index=True)
            self.users_df.to_csv(DATASET_URL + 'users.csv')
            ret = True
        else:
            # GO BACK 
            print("acc < threshold")

        return ret

    def train_new_data(self, X_train, X_test, y_train, y_test):
        params = {"C": 36.77783910335444, "kernel":"rbf", "degree": 8, "gamma": 1.7575790771023974}
        clf = util.init_model('svm', params)
        
        start_time = time.time()
        clf.fit(X_train.values, y_train.values)
        print("--- %s seconds ---" % (time.time() - start_time))

        y_pred = clf.predict(X_test.values)
        cm = confusion_matrix(y_test.values, y_pred)
        acc_score = self.model_testing(cm, y_pred, y_test)

        return (clf, acc_score)

    def model_testing(self, cm, y_pred, y_test):
        acc_score = accuracy_score(y_test.values, y_pred)
        print(cm)
        print(classification_report(y_test.values, y_pred))
        print('accuracy_score ', acc_score)
        print('cohen_kappa_score ', cohen_kappa_score(y_test.values, y_pred))
        print('f1_score ', f1_score(y_test.values, y_pred, average='macro'))
        print('precision_score ', precision_score(y_test.values, y_pred, average='macro'))
        print('recall_score ', recall_score(y_test.values, y_pred, average='macro'))
        return acc_score

    

    


    def test(self):
        video_capture = cv2.VideoCapture(0)

        while True:
            # Grab a single frame of video
            _, frame = video_capture.read()

            print(len(frame), ", ", len(self.face_encodings))

            if frame is not None:
                # Resize frame of video to 1/2 size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = small_frame[:, :, ::-1]

                if (len(self.face_encodings) < self.NEW_DATA):
                    self.capture_face(rgb_small_frame)
                else:
                    self.data_prep()
                    break

                # Display the resulting image
                cv2.imshow('Test', frame)

                # Hit 'q' on the keyboard to quit!
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        video_capture.release()
        cv2.destroyAllWindows()
