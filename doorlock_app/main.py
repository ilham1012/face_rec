from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.properties import ObjectProperty

import cv2

from face_recognizer import FaceRecognizer


class FirstScreen(Screen):
    pass

class SecondScreen(Screen):

    def update(self, dt):
        print(self.ids.cam_display.source)

class ScreenManagement(ScreenManager):
    first_screen = ObjectProperty(None)
    second_screen = ObjectProperty(None)


Builder.load_file("main_tes.kv")

class MainApp(App):
    odd = True

    # Const
    # Threshold for face recognition confidence score
    THRESHOLD = 0.85
    RESIZE_FACTOR = 4
    FRAME_SKIPPING = 10

    frame_idx = 0

    def build(self):
        self.capture = cv2.VideoCapture(0)
        cv2.namedWindow("CV2 Image")
        Clock.schedule_interval(self.update, 1.0/30.0)
        self.root = ScreenManagement()
        self.fr = FaceRecognizer('svm')
        return self.root

    def update(self, dt):
        if (self.root.current == 'second_screen'):
            frame, clf_result, face_locations, faces_landmarks = self.process_video()
            self.display_video(frame)

        self.odd = not self.odd
        # print('Current: ', self.sm.current)


    def process_video(self):
        clf_result = (None, None)
        face_locations = None
        faces_landmarks = None

        _, frame = self.capture.read()
        cv2.imshow("CV2 Image", frame)

        # Resize frame of video to 1/2 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=1/self.RESIZE_FACTOR, fy=1/self.RESIZE_FACTOR)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        # if odd_frame:
        if self.frame_idx == self.FRAME_SKIPPING:
            # print("process!")
            self.frame_idx = 0
            clf_result = self.fr.recognize_face(rgb_frame)

            name, max_prob = clf_result

            print("-----")
            print("Name: ", name[0], " ", max_prob[0])

            # Open the door if name is not "Unknown" and prob > Threshold
            if (name[0] != "unknown") and (max_prob[0] > self.THRESHOLD):
                print("OPEN THE DOOR")
                # result = firebase.put_async(device_url, 'lock', False, callback=relock)
                # result = firebase.put(device_url, 'lock', False)
                # relock(result)
                
            print("-----")
            
        else:
            self.frame_idx += 1

        return frame, clf_result, face_locations, faces_landmarks

    def display_video(self, frame):
        app = App.get_running_app()
        
        # convert it to texture
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        
        # display image from the texture
        app.root.second_screen.ids.cam_display.texture = texture1
        



if __name__ == '__main__':
    MainApp().run()