import time

import cv2
import numpy as np
import face_recognition
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, auc, cohen_kappa_score, f1_score, precision_score, recall_score
import joblib

from utils import constant, util

class RegisterFace():
    NEW_DATA = 125

    prev_train_dataset = None
    new_train_dataset = None
    prev_test_dataset = None
    new_test_dataset = None
    
    username = None
    face_encodings = []

    def __init__(self, username):
        self.username = username
        self.prev_train_dataset = util.load_data('doorlock_app/dataset/face_encodings__train.csv')
        self.prev_test_dataset = util.load_data('doorlock_app/dataset/face_encodings__test.csv')
    
    def capture_face(self, rgb_frame, model="hog"):
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame, model=model)
        
        # Make sure there is ONE face detected
        if (len(face_locations) == 1):
            face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
            self.face_encodings.append(face_encoding)

    def data_prep(self):
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
        clf = self.train_new_data(X_train, X_test, y_train, y_test)
        # Save new datasets (overwrite)
        self.new_train_dataset.to_csv(r'doorlock_app/dataset/face_encodings__train_.csv', index=False)
        self.new_test_dataset.to_csv(r'doorlock_app/dataset/face_encodings__test_.csv', index=False)
        # Save model (overwrite)
        joblib.dump(clf, 'doorlock_app/dataset/model_.pkl')

    def train_new_data(self, X_train, X_test, y_train, y_test):
        params = {"C": 36.77783910335444, "kernel":"rbf", "degree": 8, "gamma": 1.7575790771023974}
        clf = util.init_model('svm', params)
        
        start_time = time.time()
        clf.fit(X_train.values, y_train.values)
        print("--- %s seconds ---" % (time.time() - start_time))

        y_pred = clf.predict(X_test.values)
        cm = confusion_matrix(y_test.values, y_pred)
        self.print_testing(cm, y_pred, y_test)

        return clf

    def print_testing(self, cm, y_pred, y_test):
        print(cm)
        print(classification_report(y_test.values, y_pred))
        print('accuracy_score ', accuracy_score(y_test.values, y_pred))
        print('cohen_kappa_score ', cohen_kappa_score(y_test.values, y_pred))
        print('f1_score ', f1_score(y_test.values, y_pred, average='macro'))
        print('precision_score ', precision_score(y_test.values, y_pred, average='macro'))
        print('recall_score ', recall_score(y_test.values, y_pred, average='macro'))


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
