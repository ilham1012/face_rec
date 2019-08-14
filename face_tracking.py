from collections import Counter

import cv2
import numpy as np
import scipy.spatial as spatial
import dlib
import face_recognition

from utils.iou_trackers.iou_tracker import track_iou


# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.
RESIZE_FACTOR = 2
MAX_CENTROID_DISTANCE = 50

# Get a reference to webcam #0 (the default one)
# video_capture = cv2.VideoCapture("http://admin:iit19@192.168.236.250:8080/stream/video/mjpeg")
video_capture = cv2.VideoCapture(0)

process_this_frame =  True
tracked_faces = []
tracked_centroids = []
kdtree = None

class Face(object):
    uuid = None
    startX = -1000
    startY = -1000
    endX = -1000
    endY = -1000
    centroid = -1000

    def calc_centroid(self, rect):
        (startY, endX, endY, startX) = rect
        centroidX = int((endX - startX) / 2) + startX
        centroidY = int((endY - startY) / 2) + startY

        centroid = (centroidX, centroidY)

        return centroid

    def update_location(self, rect):
        (self.startY, self.endX, self.endY, self.startX) = rect
        self.centroid = calc_centroid(rect)
    
    def __init__(self, location):
        self.update_location(location)



def check_distance(centroid1, centroid2):
    a = np.array(centroid1)
    b = np.array(centroid2)

    dist = np.linalg.norm(a-b)
    # print('dist: ', dist)

    if dist < MAX_CENTROID_DISTANCE:
        return dist
    else:
        return 1000




def calc_centroid(rect):
    (startY, endX, endY, startX) = rect
    centroidX = int((endX - startX) / 2) + startX
    centroidY = int((endY - startY) / 2) + startY

    centroid = (centroidX, centroidY)

    return centroid


# VIS
def my_filled_circle(img, center):
    center = tuple([RESIZE_FACTOR * x for x in center])
    cv2.circle(img, center, 2, (255, 200, 255))

def display_box(rect, name='0'):
    (startY, endX, endY, startX) = rect
    text = "face #" + name
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.rectangle(frame, (RESIZE_FACTOR * startX, RESIZE_FACTOR * startY), (RESIZE_FACTOR * endX, RESIZE_FACTOR * endY), (0, 0, 255), 2)
    cv2.putText(frame, text, (startX + 20, startY + 20), font, 1.0, (0, 0, 255), 1)



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
        
        centroidX = None
        centroidY = None
        centroid  = None

        face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
        dets = []

        # ensure at least one detection is made
        if len(face_locations) > 0:
            for location in face_locations:
                display_box(location)
                dets.append({'bbox': (location[3], location[0], location[1], location[2]), 'score': 1})

            # print(dets)

            tracks = track_iou([dets], 0.0, 0.99, 0.3, 3)

            print(tracks)

        #     if len(tracked_faces) == 0:
        #         # if no tracked face yet, add all
        #         for location in face_locations:
        #             detected_face = Face(location)

        #             tracked_faces.append(detected_face)
                
        #         print('tracked: ', tracked_faces)

        #     else:
        #         # Match existing Face objects with a Rectangle
        #         print("tracked: ", len(tracked_faces), " - detected: ", len(face_locations))

        #         # closest_face = None
        #         # closest_dist = 999
        #         n_distances = []
        #         n_ids = []
        #         n_id0 = []


        #         for location in face_locations:
        #             n_distance, n_id = kdtree.query(calc_centroid(location), k=3)
        #             n_distances.append(n_distance)
        #             n_ids.append(n_id)
        #             n_id0.append(n_id[0])

        #         # print(n_ids)
                
        #         counter = Counter(n_id0)
        #         print(counter)
                
                    

        #             # for t in tracked_faces:
        #             #     dist = check_distance(t.centroid, calc_centroid(location))
        #             #     # print('check distance: ', dist)

        #             #     # Find faces[index] that is closest to face f
        #             #     # set used[index] to true so that it can't be used twice
        #             #     if (dist < closest_dist):
        #             #         # Update Face object location
        #             #         closest_dist = dist
        #             #         closest_face = t
        #             #     else:
        #             #         detected_face = Face(location)
        #             #         tracked_faces.append(detected_face)


        #     for t in tracked_faces:
        #         # display_box(t.rect, str(id(t)))
        #         tracked_centroids.append(t.centroid)

        #     kdtree = spatial.KDTree(tracked_centroids)
                
        

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
