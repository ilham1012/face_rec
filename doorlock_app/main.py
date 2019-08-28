import cv2
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, CardTransition
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.properties import ObjectProperty

from utils.util import calc_centroid
# from face_recognizer import FaceRecognizer
from doorlock_app.scan_screen import ScanScreen
from doorlock_app.result_screen import ResultScreen


Builder.load_file("kv/main.kv")


class FrontScreen(Screen):
    pass

class ScreenManagement(ScreenManager):
    front_screen = ObjectProperty(None)
    scan_screen = ObjectProperty(None)
    result_screen = ObjectProperty(None)

class MainApp(App):
    frame_status = "pre" # ['pre', 'on', 'post']
    frame_idx = 0
    name = ""

    # Const
    PRE_FRAME = 30
    POST_FRAME = 45
    FRAME_SKIPPING = 10

    def build(self):
        self.capture = cv2.VideoCapture(0)
        cv2.namedWindow("CV2 Image")
        Clock.schedule_interval(self.update, 1.0/30.0)
        self.root = ScreenManagement() # (transition=CardTransition())
        # self.fr = FaceRecognizer()
        self.app = App.get_running_app()
        return self.root

    def update(self, dt):
        if (self.root.current == 'scan_screen'):
            frame = self.stream_video()
            self.display_video(frame)
        # print('Current: ', self.sm.current)

    def stream_video(self):
        #clf_result = (None, None)

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
                _ = self.root.scan_screen.process_video(frame, self.app)
            else:
                self.frame_idx += 1

        return frame #, clf_result

    def display_video(self, frame):
        # convert it to texture
        texture1 = self.frame_to_texture(frame)
        # display image from the texture
        self.root.scan_screen.ids.cam_display.texture = texture1

    def frame_to_texture(self, frame):
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        return texture    
    

if __name__ == '__main__':
    MainApp().run()