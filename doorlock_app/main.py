import time

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, CardTransition
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.properties import ObjectProperty

import cv2

from face_recognizer import FaceRecognizer


class FrontScreen(Screen):
    pass

class ScanScreen(Screen):
    def reset(self):
        self.ids.info_text.text = "Pastikan wajah tidak tertutupi"

    def face_detected(self):
        self.ids.info_text.text = "Terdeteksi!"

class ResultScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.display_screen)

    def display_screen(self, dt):
        app = App.get_running_app()
        print('sleep')
        time.sleep(5)
        print('wakeup')
        print(app.root.current)
        app.root.current = 'front_screen'

    def update_screen(self, name, score, crop_texture):
        if (name != "unknown"):
            txt1 = "Wajah dikenali"
            txt2 = "Selamat Datang"
            self.open_door()
        else:
            txt1 = "Wajah terdeteksi"
            txt2 = "Maaf Anda Tidak Terdaftar"

        txt3 = name.capitalize()
        txt4 = "Confidence score: {:2.0f}%".format(score*100)

        self.ids.img_display.ids.crop_img.texture = crop_texture
        self.ids.info_text.text = txt1
        self.ids.info_text_2.text = txt2
        self.ids.info_text_3.text = txt3
        self.ids.info_text_4.text = txt4
        

    def open_door(self):
        print("OPEN THE DOOR")
        # result = firebase.put_async(device_url, 'lock', False, callback=relock)
        # result = firebase.put(device_url, 'lock', False)
        # relock(result)
    

class ScreenManagement(ScreenManager):
    front_screen = ObjectProperty(None)
    scan_screen = ObjectProperty(None)
    result_screen = ObjectProperty(None)


Builder.load_file("kv/main.kv")

class MainApp(App):
    frame_status = "pre" # ['pre', 'on', 'post']
    frame_idx = 0
    name = ""
    
    odd = True

    # Const
    # Threshold for face recognition confidence score
    THRESHOLD = 0.85
    RESIZE_FACTOR = 4
    PRE_FRAME = 30
    POST_FRAME = 45
    FRAME_SKIPPING = 10

    def build(self):
        self.capture = cv2.VideoCapture(0)
        cv2.namedWindow("CV2 Image")
        Clock.schedule_interval(self.update, 1.0/30.0)
        self.root = ScreenManagement() # (transition=CardTransition())
        self.fr = FaceRecognizer('svm')
        return self.root

    def update(self, dt):
        if (self.root.current == 'scan_screen'):
            frame, clf_result = self.stream_video()
            self.display_video(frame)

        self.odd = not self.odd
        # print('Current: ', self.sm.current)


    def stream_video(self):
        # process_frame = False

        clf_result = (None, None)

        _, frame = self.capture.read()
        cv2.imshow("CV2 Image", frame)        

        print(self.frame_status, " : ", self.frame_idx)

        if (self.frame_status == 'pre'):
            if self.frame_idx == self.PRE_FRAME:
                self.frame_idx = 0
                self.frame_status = 'on'
            else:
                self.frame_idx += 1

        elif (self.frame_status == 'post'):
            if self.frame_idx == self.POST_FRAME:
                self.frame_idx = 0
                self.frame_status = 'pre'
                self.root.current = 'result_screen'                     
                self.root.scan_screen.reset()
            else:
                self.frame_idx += 1

        else:
            # Only process every n frame of video to save time
            if self.frame_idx == self.FRAME_SKIPPING:
                self.frame_idx = 0
                clf_result = self.process_video(frame)
            else:
                self.frame_idx += 1

        return frame, clf_result

    def display_video(self, frame):
        app = App.get_running_app()        
        # convert it to texture
        texture1 = self.frame_to_texture(frame)
        # display image from the texture
        app.root.scan_screen.ids.cam_display.texture = texture1

    def frame_to_texture(self, frame):
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        return texture    
    
    def process_video(self, frame):
        # Resize frame of video to 1/2 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=1/self.RESIZE_FACTOR, fy=1/self.RESIZE_FACTOR)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = small_frame[:, :, ::-1]

        # print("process!")
        clf_result = self.fr.recognize_face(rgb_frame, False)

        names, max_prob = clf_result

        if (names is not None):
            print("-----")
            print("Name: ", names[0], " ", max_prob[0])

            # Open the door if name is not "Unknown" and prob > Threshold
            if (max_prob[0] > self.THRESHOLD):
                self.name = names[0]
                centroidX, centroidY = self.calc_centroid(self.fr.face_locations[0])
                
                centroidX *= self.RESIZE_FACTOR                
                centroidY *= self.RESIZE_FACTOR

                top = centroidY - 100 if centroidY >= 100 else 0
                bottom = centroidY + 100 if centroidY < frame.shape[1] else frame.shape[1]
                left = centroidX - 100 if centroidX >= 100 else 0
                right = centroidX + 100 if centroidX < frame.shape[0] else frame.shape[0]

                crop_img = frame[top:bottom, left:right]
                crop_texture = self.frame_to_texture(crop_img)

                self.root.scan_screen.face_detected()
                self.frame_idx = 0
                self.frame_status = 'post'
                self.root.result_screen.update_screen(self.name, max_prob[0], crop_texture)
                
            print("-----")

        return clf_result

    def calc_centroid(self, rect):
        (startY, endX, endY, startX) = rect
        centroidX = int((endX - startX) / 2) + startX
        centroidY = int((endY - startY) / 2) + startY

        centroid = (centroidX, centroidY)

        return centroid


if __name__ == '__main__':
    MainApp().run()