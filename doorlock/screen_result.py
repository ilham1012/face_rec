import time

import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image
from PIL import ImageTk
import cv2
# import RPi.GPIO as GPIO

from doorlock.constants import ASSETS_URL
from doorlock.styles import colors

class ResultScreen(tk.Frame):
    output_pin = 18

    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)

        self['bg'] = colors['navy']

        self.GPIO_init()

        self.title_txt = tk.StringVar()
        self.subtitle_txt = tk.StringVar()

        self.title = ttk.Label(self, textvariable=self.title_txt, style='Title.TLabel')
        self.subtitle = ttk.Label(self, textvariable=self.subtitle_txt, style='Subtitle.TLabel')
        self.title.pack(pady=10, padx=10)
        self.subtitle.pack(pady=10, padx=10)
        
        self.panel = tk.Label(self, bd=0, highlightthickness=0)
        self.panel.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.app = app

    def show_screen(self):
        print("[SHOW SCREEN] Result")
        self.GPIO_init()
        # try:
        #     print("GPIO.HIGH")
        #     GPIO.output(self.output_pin, GPIO.HIGH)
        #     print("Sleep")
        time.sleep(2)
        #     print("GPIO.LOW")
        #     GPIO.output(self.output_pin, GPIO.LOW)
        # finally:
        #     GPIO.cleanup()
        self.app.show_frame("home")

    def update_info(self, name, prob, img):
        self.name = name
        self.prob = prob
        # self.img = img
        txt_title = "Welcome " + name.capitalize()
        txt_subtitle = "Confidence score: {:2.0f}%".format(prob*100)

        self.title_txt.set(txt_title)
        self.subtitle_txt.set(txt_subtitle)

        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        self.panel.configure(image=image)
        self.panel.image = image

    def GPIO_init(self):
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(self.output_pin, GPIO.OUT, initial=GPIO.LOW)
        pass
