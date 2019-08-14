__author__ = 'bunkus'
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

import cv2
import numpy as np

class CamApp(App):

    def build(self):
        self.img1 = Image(source='images/1.jpg')
        layout = BoxLayout()
        layout.add_widget(self.img1)
        #opencv2 stuffs
        self.capture = cv2.VideoCapture(0)
        ret, frame = self.capture.read()
        cv2.namedWindow("CV2 Image")
        cv2.imshow("CV2 Image", frame)
        Clock.schedule_interval(self.update, 1.0/33.0)
        return layout
    
    def update(self, dt):
        # display image from cam in opencv window
        ret, frame = self.capture.read()
        cv2.imshow("CV2 Image", frame)
        # convert it to texture
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.img1.texture = texture1
        print(texture1)
    
    # def CreateImage(self, size, bits=np.uint8, channels=3, color=(0, 0, 0)): # (cv.GetSize(frame), 8, 3)
    #     """Create new image(numpy array) filled with certain color in RGB"""
    #     height, width = size
    #     # Create black blank image
    #     if bits == 8:
    #         bits = np.uint8
    #     elif bits == 32:
    #         bits = np.float32
    #     elif bits == 64:
    #         bits = np.float64
    #     image = np.zeros((height, width, channels), bits)
    #     if color != (0, 0, 0):
    #         # Fill image with color
    #         image[:] = color
    #     return image
        
if __name__ == '__main__':
    CamApp().run()