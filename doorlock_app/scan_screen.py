import cv2
from kivy.uix.screenmanager import ScreenManager, Screen

from utils.util import calc_centroid
from face_recognizer import FaceRecognizer

class ScanScreen(Screen):
    THRESHOLD = 0.85
    RESIZE_FACTOR = 4
    fr = FaceRecognizer()

    def reset(self):
        self.ids.info_text.text = "Pastikan wajah tidak tertutupi"

    def face_detected(self):
        self.ids.info_text.text = "Terdeteksi!"

    def process_video(self, frame, app):
        # Resize frame of video to 1/2 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=1/self.RESIZE_FACTOR, fy=1/self.RESIZE_FACTOR)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = small_frame[:, :, ::-1]

        # print("process!")
        clf_result = self.fr.recognize_face(rgb_frame, False)

        names, max_prob = clf_result

        print("App: ", app)

        if (names is not None):
            print("-----")
            print("Name: ", names[0], " ", max_prob[0])

            # Open the door if name is not "Unknown" and prob > Threshold
            if (max_prob[0] > self.THRESHOLD):
                app.name = names[0]
                centroidX, centroidY = calc_centroid(self.fr.face_locations[0])
                
                centroidX *= self.RESIZE_FACTOR
                centroidY *= self.RESIZE_FACTOR

                top = centroidY - 100 if centroidY >= 100 else 0
                bottom = centroidY + 100 if centroidY < frame.shape[1] else frame.shape[1]
                left = centroidX - 100 if centroidX >= 100 else 0
                right = centroidX + 100 if centroidX < frame.shape[0] else frame.shape[0]

                crop_img = frame[top:bottom, left:right]
                crop_texture = app.frame_to_texture(crop_img)

                self.face_detected()
                app.frame_idx = 0
                app.frame_status = 'post'
                app.root.result_screen.update_screen(app.name, max_prob[0], crop_texture)
                
            print("-----")

        return clf_result