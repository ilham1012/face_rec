from __future__ import print_function

import os
import time
import datetime
import threading

import cv2
import pandas as pd
from PIL import Image
from PIL import ImageTk
import tkinter as tk
import imutils
from imutils.video import VideoStream
import RPi.GPIO as GPIO

from utils.util import calc_centroid
from face_recognizer import FaceRecognizer
from doorlock.screen_home import HomeScreen
from doorlock.screen_scan import ScanScreen
from doorlock.screen_result import ResultScreen
from doorlock.screen_login import LoginScreen
from doorlock.screen_admin_login import AdminLoginScreen
from doorlock.screen_registration import RegistrationScreen
from doorlock.screen_scan_new import ScanNewScreen
from doorlock.constants import LARGE_FONT, MEDIUM_FONT, DATASET_URL
from doorlock.styles import init_style



class App(tk.Tk):
    output_pin = 12
    buzzer_pin = 18

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.on_jetson = False
        init_style()
        # init camera
        self.video_stream = VideoStream(usePiCamera=False).start()
        self.users_df  = pd.read_csv(DATASET_URL + 'users.csv')
        # init root frame
        root_frame = tk.Frame(self)
        root_frame.pack(side="top", fill="both", expand=True)
        root_frame.grid_rowconfigure(0, weight=1)
        root_frame.grid_columnconfigure(0, weight=1)
        # init screens
        self.init_screens(root_frame)
        # show default frame
        self.show_frame("home")
        # set on_close on delete window protocol
        self.wm_protocol("WM_DELETE_WINDOW", self.on_close)
        self.GPIO = GPIO
        self.GPIO_init()

    def init_screens(self, root_frame):
        self.screens = {}
        # home screen
        self.home_screen = HomeScreen(root_frame, self)
        self.screens["home"] = self.home_screen
        self.home_screen.grid(row=0, column=0, sticky="nsew")
        # scan screen
        self.scan_screen = ScanScreen(root_frame, self)
        self.screens["scan"] = self.scan_screen
        self.scan_screen.grid(row=0, column=0, sticky="nsew")
        # result screen
        self.result_screen = ResultScreen(root_frame, self)
        self.screens["result"] = self.result_screen
        self.result_screen.grid(row=0, column=0, sticky="nsew")
        # admin login screen
        self.admin_login_screen = AdminLoginScreen(root_frame, self)
        self.screens["admin_login"] = self.admin_login_screen
        self.admin_login_screen.grid(row=0, column=0, sticky="nsew")
        # login screen
        self.login_screen = LoginScreen(root_frame, self)
        self.screens["login"] = self.login_screen
        self.login_screen.grid(row=0, column=0, sticky="nsew")
        # registration screen
        self.registration_screen = RegistrationScreen(root_frame, self, self.users_df)
        self.screens["registration"] = self.registration_screen
        self.registration_screen.grid(row=0, column=0, sticky="nsew")
        # scan_new screen
        self.scan_new_screen = ScanNewScreen(root_frame, self, self.users_df)
        self.screens["scan_new"] = self.scan_new_screen
        self.scan_new_screen.grid(row=0, column=0, sticky="nsew")

        
        print("SCREENS")
        print(self.screens)

    def show_frame(self, screen_class):
        screen = self.screens[screen_class]
        screen.tkraise()
        screen.update()
        screen.show_screen()

    def on_close(self):
        self.video_stream.stop()
        print("[INFO] Close App")
        GPIO.cleanup()
        self.quit()

    def GPIO_init(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.buzzer_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.output_pin, GPIO.OUT, initial=GPIO.LOW)
        # init fallback
        self.app.GPIO.output(self.buzzer_pin, 0)
        self.app.GPIO.output(self.output_pin, 0)
        # pass


app = App()
app.geometry("800x480")
app.mainloop()
