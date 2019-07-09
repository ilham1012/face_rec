import face_recognition
from os import walk
import argparse
import pandas as pd
import numpy as np


# Generate Features (Landmarks and Encodings)
# ----------
# The code extracts Landmarks and Encodings of the faces
# Then save it to the csv file
# We use the Encodings as the feature for the classifier
# Landmarks used for exploration (?)



dataset_path = "bpi/"

faces_landmarks = []
faces_encodings = []

# Loop for each person
for (dirpath, dirnames, filenames) in walk(dataset_path):

    for dirname in dirnames:
        print('**********')
        print(dirname)
        print('**********')
        
        # ---------------------
        # List all the filename in folder
        # ---------------------
        f = []

        # loop for each photo of the person
        for (dirpath, dirnames, filenames) in walk(dataset_path + dirname):
            print('----------')
            print(dataset_path + dirname)
            print(filenames)
            print('----------')

            f.extend(filenames)
            break

        # print("files in folder:" + str(len(f)))


        for pic in f:
            # load image
            image = face_recognition.load_image_file(dataset_path + dirname + "/" + pic)

            # ---------------------
            # extract face landmark
            # ---------------------
            faces_landmark = face_recognition.face_landmarks(image)
            if (len(faces_landmark) == 0):
                print("No landmark in: " + dirname + "/" + pic)
            else:
                for landmark in faces_landmark:
                    landmark["name"] = str(dirname)
                    faces_landmarks.append(landmark)

            # ------------------
            # extract encoding
            # ------------------
            face_encodings = face_recognition.face_encodings(image)
            if (len(face_encodings) == 0):
                print("No encodings in: " + dirname + "/" + pic)
            else:
                for encoding in face_encodings:
                    lst = list(encoding)
                    lst.append(dirname)
                    faces_encodings.append(lst)

    print("total landmarks: " + str(len(faces_landmarks)))


# ------------------
# Landmark DataFrame
# ------------------
df = pd.DataFrame(faces_landmarks)
# Reorder columns
cols = ['bottom_lip', 'chin', 'left_eye', 'left_eyebrow', 'nose_bridge', 'nose_tip', 'right_eye', 'right_eyebrow', 'top_lip', 'name']
df = df[cols]


# ------------------
# Encoding DataFrame
# ------------------
df2 = pd.DataFrame(faces_encodings)
# Rename column name
df2.rename(columns={'128':'name'}, inplace=True)
print(df2.columns)

# Save to CSV
df.to_csv(r'dataset/face_landmarks.csv')
df2.to_csv(r'dataset/face_encodings.csv')