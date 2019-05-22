import face_recognition
from os import walk
import argparse
import pandas as pd
import numpy as np


# names = ["test"]
names = ["rian", "aris", "jony", "unknown"]
faces_landmarks = []
faces_encodings = []

# Loop for each person
for name in names:
    f = []

    # loop for each photo of the person
    for (dirpath, dirnames, filenames) in walk("dataset/" + name):
        f.extend(filenames)
        break

    # print("files in folder:" + str(len(f)))


    for pic in f:
        # load image
        image = face_recognition.load_image_file("dataset/" + name + "/" + pic)

        # ---------------------
        # extract face landmark
        # ---------------------
        faces_landmark = face_recognition.face_landmarks(image)
        if (len(faces_landmark) == 0):
            print("No landmark in: " + name + "/" + pic)
        else:
            for landmark in faces_landmark:
                landmark["name"] = str(name)
                faces_landmarks.append(landmark)

        # ------------------
        # extract encoding
        # ------------------
        face_encodings = face_recognition.face_encodings(image)
        if (len(face_encodings) == 0):
            print("No encodings in: " + name + "/" + pic)
        else:
            for encoding in face_encodings:
                lst = list(encoding)
                lst.append(name)
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