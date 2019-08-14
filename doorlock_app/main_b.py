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


class MainScreen(Screen):
    pass

class FaceScanScreen(Screen):
    pass

class ScreenManagement(ScreenManager):
    main_screen = ObjectProperty(None)
    face_scan_screen = ObjectProperty(None)


Builder.load_file("main.kv")

class MainApp(App):
    def build(self):
        # self.stuff_p.ids.cam_display.source = 'test.jpg'
        # cam_display = Image(source='test.jpg')
        # self.root.cam_canvas.add_widget(cam_display)
        # layout = BoxLayout()
        # layout.add_widget(self.img1)
        #opencv2 stuffs
        self.capture = cv2.VideoCapture(0)
        cv2.namedWindow("CV2 Image")
        Clock.schedule_interval(self.update, 1.0/33.0)
        self.root = ScreenManagement()
        return self.root

    def update(self, dt):
        # pass
        # print('Current: ', self.sm.current)
        app = App.get_running_app()

        app.root.main_screen.ids.info_text.text = 'Ah euy!'
        print(app.root.main_screen.ids.info_text.text)
        
        if (self.root.current == 'face_scan_screen'):
            
            _, frame = self.capture.read()
            cv2.imshow("CV2 Image", frame)
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            print(frame)
            # display image from the texture
            # self.cam_display.texture = texture1
            print(app.root.face_scan_screen.ids.cam_canvas.cam_display.texture)
            app.root.face_scan_screen.ids.cam_canvas.cam_display.source = 'test2.jpg'
            app.root.face_scan_screen.ids.cam_canvas.label_display.text = 'zzzzzz'

if __name__ == '__main__':
    MainApp().run()
    cv2.destroyAllWindows()