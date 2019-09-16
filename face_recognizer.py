import time
import sys

import cv2
import numpy as np
import face_recognition
from sklearn.externals import joblib

from utils import constant


class FaceRecognizer():
    """Face Recognizer Class.

    ...

    Methods
    -------
    recognize_face(rgb_frame)
        Recognize face name and probability given rgb_frame.
    """

    # Initialize some variables
    face_locations = []
    face_encodings = []
    faces_landmarks = []
    face_names = []
    
    def __init__(self, clasifier="default"):
        """Init the recognizer's clasifier model"""

        # Set classifier model
        # Models: Decision Tree, SVM, Random Forest, Adaboost
        if (clasifier == constant.MODELS[0]): #dt
            self.model_file = 'models/dt__2019-07-16_14-08-52.pkl'
        elif (clasifier == constant.MODELS[1]): #svm
            self.model_file = 'models/svm__2019-07-16_14-09-42.pkl'
        elif (clasifier == constant.MODELS[2]): #rf
            self.model_file = 'models/rf__2019-07-16_14-10-34.pkl'
        elif (clasifier == constant.MODELS[3]): #Adaboost
            self.model_file = 'models/ada__2019-07-16_14-11-06.pkl'
        elif (clasifier == "default"):
            self.model_file = 'doorlock_app/models/model.pkl'
        else:
            self.model_file = clasifier

        self.load_model()

    def load_model(self):
        self.clf = joblib.load(self.model_file)


    def recognize_face(self, rgb_frame, multiface=True, model="hog"):
        """Main function of face recognition of this class.

        Parameters
        ----------
        rgb_frame : numpy array
            frame from camera with RGB color format
        
        multiface : bool (default True)
            allow to recognize > 1 face
        
        model : string (choose ["hog", "cnn"]; default "hog")
            face detection and bounding box model: Histogram Oriented Gradient or CNN-based model

        Returns
        -------
        clf_result : (str list, num list)
            Classifier result, contains names and probabilities
        """

        names  = None
        max_probs = None

        # Find all the faces and face encodings in the current frame of video
        self.face_locations = face_recognition.face_locations(rgb_frame, model=model)

        # Make sure there are face detected
        if (len(self.face_locations) > 0):

            if (multiface):
                # Allow multiface recognition
                names, max_probs = self.__recognize_process(rgb_frame, self.face_locations)
            else:
                # Make sure to process if only 1 face detected
                if (len(self.face_locations) == 1):
                    names, max_probs = self.__recognize_process(rgb_frame, self.face_locations)           
            
        return (names, max_probs)


    def __recognize_process(self, rgb_frame, face_locations):
        self.faces_landmarks = face_recognition.face_landmarks(rgb_frame, self.face_locations)
        self.face_encodings = face_recognition.face_encodings(rgb_frame, self.face_locations)
        
        # Clasify with probabilities of each prediction
        prob = self.clf.predict_proba(self.face_encodings)

        # Get names and probs of top prediction
        max_prob_idx = prob.argmax(axis=1)
        names = self.clf.classes_[max_prob_idx]
        max_probs = prob[0][max_prob_idx]

        return (names, max_probs)