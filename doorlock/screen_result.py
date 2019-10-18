import time
from datetime import datetime
import json

import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image
from PIL import ImageTk
import cv2
# import RPi.GPIO as GPIO
from firebase import firebase

from doorlock.constants import ASSETS_URL
from doorlock.styles import colors

class ResultScreen(tk.Frame):
    output_pin = 12

    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)

        self['bg'] = colors['navy']
        self.title_up_txt = tk.StringVar()
        self.title_down_txt = tk.StringVar()
        self.sub_up_txt = tk.StringVar()
        self.sub_down_txt = tk.StringVar()

        self.title_up = ttk.Label(self, textvariable=self.title_up_txt, style='TitleB.TLabel')
        self.title_down = ttk.Label(self, textvariable=self.title_down_txt, style='TitleB.TLabel')
        self.sub_up = ttk.Label(self, textvariable=self.sub_up_txt, style='Subtitle.TLabel')
        self.sub_down = ttk.Label(self, textvariable=self.sub_down_txt, style='Subtitle.TLabel')
        
        self.sub_up.place(relx=.5, rely=0.15, anchor=tk.S)
        self.title_up.place(relx=.5, rely=0.215, anchor=tk.S)
        self.title_down.place(relx=.5, rely=0.785, anchor=tk.S)
        self.sub_down.place(relx=.5, rely=0.85, anchor=tk.S)
        
        self.panel = tk.Label(self, bd=0, highlightthickness=0)
        self.panel.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.app = app
        self.fb = firebase.FirebaseApplication('https://lab-iit.firebaseio.com/', None)

    def show_screen(self):
        print("[SHOW SCREEN] Result")

        if (self.name != "unknown"):
            # self.app.GPIO.output(self.output_pin, 1)
            result = self.fb.put_async('/test1/pintu/', 'lock', False) # callback=relock
            print('unlock:', result)
            time.sleep(3)
            result = self.fb.put_async('/test1/pintu/', 'lock', True)
            print('relock:', result)
            # self.app.GPIO.output(self.output_pin, 0)
            self.log_opener()
        else:
            time.sleep(2)

        self.reset()
        self.app.show_frame("home")

    def log_opener(self):
        dtime = datetime.now()
        dtime_str = dtime.strftime("%d/%m/%Y, %H:%M:%S")

        rec_str = '{"username": "'+ self.name +'", "datetime": "' + dtime_str + '" }'
        rec_json = json.loads(rec_str)
        result = self.fb.post('/test1/pintu/logs', rec_json)
        print(result)

    def reset(self):
        self.name = ""
        self.prob = 0
        self.title_up_txt.set("")
        self.title_down_txt.set("")
        self.sub_up_txt.set("")
        self.sub_down_txt.set("")

    def update_info(self, name, prob=0, img=[], mode=0):
        self.name = name
        self.prob = prob

        if (name == "unknown"):
            txt_title_up = "Maaf Anda Tidak Terdaftar"
            txt_title_down = "Unknown"
        else:
            user_query = self.app.users_df[self.app.users_df.username == name]
            full_name = user_query.full_name.item()
            txt_title_up = "Selamat Datang"
            txt_title_down = full_name.title()

        if (mode == 0):
            txt_sub_up = "Wajah Dikenali"
            txt_sub_down = "Confidence score: {:2.0f}%".format(prob*100)
        else:
            txt_sub_up = "Akun Dikenali"
            txt_sub_down = "Masuk dengan Password"

        
        print("[RESULT] MODE: ", mode)
        print(txt_sub_up)
        print(txt_title_up)
        print(txt_title_down)
        print(txt_sub_down)

        self.title_up_txt.set(txt_title_up)
        self.sub_up_txt.set(txt_sub_up)
        self.title_down_txt.set(txt_title_down)
        self.sub_down_txt.set(txt_sub_down)

        if (img == []):
            image = Image.open(ASSETS_URL + 'img/face_fallback.png')
        else:
            image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)

        image = ImageTk.PhotoImage(image)
        self.panel.configure(image=image)
        self.panel.image = image