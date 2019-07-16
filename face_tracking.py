import cv2
import numpy as np
import dlib
import face_recognition


# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.
RESIZE_FACTOR = 2

# Get a reference to webcam #0 (the default one)
# video_capture = cv2.VideoCapture("http://admin:iit19@192.168.236.250:8080/stream/video/mjpeg")
video_capture = cv2.VideoCapture(1)

process_this_frame =  True
trackers = []

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    # print("ret: ", ret)
    # print("frame: ", frame)

    if frame is not None:

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=1/RESIZE_FACTOR, fy=1/RESIZE_FACTOR)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]


        if len(trackers) == 0:
            face_locations = face_recognition.face_locations(rgb_small_frame)

            # ensure at least one detection is made
            if len(face_locations) > 0:
                for face in face_locations:
                    (startY, endX, endY, startX) = face

                    # construct a dlib rectangle object from the bounding
                    # box coordinates and then start the dlib correlation
                    # tracker
                    tracker = dlib.correlation_tracker()
                    rect = dlib.rectangle(startX, startY, endX, endY)
                    # print(rect)
                    tracker.start_track(rgb_small_frame, rect)
                    trackers.append(tracker)

                    startX *= RESIZE_FACTOR
                    startY *= RESIZE_FACTOR
                    endX *= RESIZE_FACTOR
                    endY *= RESIZE_FACTOR

                    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    text = "face #" + str(len(trackers) - 1)
                    cv2.putText(frame, text, (startX + 20, startY + 20), font, 1.0, (0, 0, 255), 1)
        else:
            # loop over each of the trackers
            # for (t, l) in zip(trackers, labels):
            for idx, t in enumerate(trackers):
                # update the tracker and grab the position of the tracked
                # object
                t.update(rgb_small_frame)
                pos = t.get_position()
    
                # unpack the position object
                startX = int(pos.left())
                startY = int(pos.top())
                endX = int(pos.right())
                endY = int(pos.bottom())

                startX *= RESIZE_FACTOR
                startY *= RESIZE_FACTOR
                endX *= RESIZE_FACTOR
                endY *= RESIZE_FACTOR

                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
                font = cv2.FONT_HERSHEY_DUPLEX
                text = "face #" + str(idx)
                cv2.putText(frame, text, (startX + 20, startY + 20), font, 1.0, (0, 0, 255), 1)

        

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
