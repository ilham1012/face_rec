import argparse
import os

import cv2
import numpy as np
import face_recognition


# Capture Face for Dataset Building
# ----------
# The code detects face(s) in the frame
# Crop according to face location detected (plus 100px offsets in each direction)
# Then save the file to the folder set in the argument parser


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True,
	help="path to output directory")
args = vars(ap.parse_args())


# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture("http://admin:iit19@192.168.222.137:8080/stream/video/mjpeg")

process_this_frame =  True
total = 0

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        print(face_locations)

    # Display the results
    for top, right, bottom, left in face_locations:
        # Draw a box around the face
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, "found", (30, 10), font, 1.0, (0, 0, 255), 1)
        top -= 100
        bottom += 100
        left -= 100
        right += 100

        crop_img = frame[top:bottom, left:right]
        p = os.path.sep.join([args["output"], "{}.png".format(
			str(total).zfill(5))])

        print(p)
        cv2.imwrite(p, crop_img)
        total += 1

       

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
