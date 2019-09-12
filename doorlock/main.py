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

from utils.util import calc_centroid
from face_recognizer import FaceRecognizer
from doorlock.screen_home import HomeScreen
from doorlock.screen_scan import ScanScreen
from doorlock.screen_result import ResultScreen
from doorlock.screen_admin_login import AdminLoginScreen
from doorlock.screen_registration import RegistrationScreen

LARGE_FONT = ("Helvetica", 18)
MEDIUM_FONT = ("Times New Roman", 16)


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.on_jetson = False
        # init camera
        self.video_stream = VideoStream(usePiCamera=False).start()
        self.users_df  = pd.read_csv(r'doorlock/users.csv')
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
        # registration screen
        self.registration_screen = RegistrationScreen(root_frame, self, self.users_df)
        self.screens["registration"] = self.registration_screen
        self.registration_screen.grid(row=0, column=0, sticky="nsew")

        
        print("SCREENS")
        print(self.screens)

    def show_frame(self, screen_class):
        screen = self.screens[screen_class]
        print(screen)
        screen.tkraise()
        screen.show_screen()

    def on_close(self):
        self.video_stream.stop()
        print("CLOSE APP")
        self.quit()


app = App()
app.geometry("800x480")
app.mainloop()
