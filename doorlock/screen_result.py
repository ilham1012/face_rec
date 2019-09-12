import time

import tkinter as tk
from PIL import Image
from PIL import ImageTk
import cv2


LARGE_FONT = ("Helvetica", 18)
MEDIUM_FONT = ("Times New Roman", 16)

class ResultScreen(tk.Frame):
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        self.title_txt = tk.StringVar()
        self.subtitle_txt = tk.StringVar()

        self.title = tk.Label(self, textvariable=self.title_txt, font=LARGE_FONT)
        self.subtitle = tk.Label(self, textvariable=self.subtitle_txt, font=MEDIUM_FONT)
        self.title.pack(pady=10, padx=10)
        self.subtitle.pack(pady=10, padx=10)
        
        self.panel = tk.Label(self)
        self.panel.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.app = app

    def show_screen(self):
        print("result")
        time.sleep(2)
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
