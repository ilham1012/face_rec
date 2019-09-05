from __future__ import print_function

import os
import time
import datetime
import threading

from PIL import Image
from PIL import ImageTk
import tkinter as tk
import imutils
from imutils.video import VideoStream
import cv2

from utils.util import calc_centroid
from face_recognizer import FaceRecognizer

LARGE_FONT = ("Helvetica", 18)
MEDIUM_FONT = ("Times New Roman", 16)


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # init camera
        self.vs = VideoStream(usePiCamera=False).start()
        # init root frame
        root_frame = tk.Frame(self)
        root_frame.pack(side="top", fill="both", expand=True)
        root_frame.grid_rowconfigure(0, weight=1)
        root_frame.grid_columnconfigure(0, weight=1)
        # init screens
        self.init_screens(root_frame)
        # show default frame
        self.show_frame(StartPage)
        # set on_close on delete window protocol
        self.wm_protocol("WM_DELETE_WINDOW", self.on_close)

    def init_screens(self, root_frame):
        self.screens = {}
        # start page
        page_start = StartPage(root_frame, self)
        self.screens[StartPage] = page_start
        page_start.grid(row=0, column=0, sticky="nsew")
        # page one
        page_one = PageOne(root_frame, self)
        self.screens[PageOne] = page_one
        page_one.grid(row=0, column=0, sticky="nsew")
        # page two
        page_two = PageTwo(root_frame, self)
        self.screens[PageTwo] = page_two
        page_two.grid(row=0, column=0, sticky="nsew")        

    def show_frame(self, screen_class):
        screen = self.screens[screen_class]
        screen_class.show_screen(screen)
        screen.tkraise()

    def on_close(self):
        self.vs.stop()
        print("CLOSE APP")
        self.quit()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        display_container = tk.Frame(self, bg="#2026A1")
        button_container = tk.Frame(self, bg="#FFFFFF", height=10)
        display_container.pack(side=tk.TOP, fill="both", expand=True)
        button_container.pack(side=tk.BOTTOM, fill="both")

        label = tk.Label(display_container, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        # img = ImageTk.PhotoImage(file="kv/img/home_img.png")
        # home_img = tk.Label(self, image=img)
        # home_img.image = img
        # home_img.pack()

        button1 = tk.Button(button_container, text="Visit Page 1",
                            command=lambda: controller.show_frame(PageOne), width=1, height=1)
        button2 = tk.Button(button_container, text="Visit Page 2",
                            command=lambda: controller.show_frame(PageTwo), width=1, height=1)
        
        button1.configure(font=MEDIUM_FONT)
        button2.configure(font=MEDIUM_FONT)
        button1.pack(side=tk.LEFT, pady=10, padx=10, fill=tk.BOTH, expand=True)
        button2.pack(side=tk.LEFT, pady=10, padx=10, fill=tk.BOTH, expand=True)

    def show_screen(self):
        print("Home")


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button2 = tk.Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(PageTwo))
        button1.pack()
        button2.pack()

    def show_screen(self):
        print("One")

class PageTwo(tk.Frame):
    frame_status = "pre" # ['pre', 'on', 'post']
    frame_idx = 0
    name = ""

    # Const
    PRE_FRAME = 30
    POST_FRAME = 45
    FRAME_SKIPPING = 10

    THRESHOLD = 0.85
    RESIZE_FACTOR = 4
    fr = FaceRecognizer()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.vs = None
        self.frame = None
        self.thread = None
        self.stopEvent = None
        self.controller = controller

        self.panel = tk.Label(self)
        self.panel.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

        label = tk.Label(self, text="Page Two", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: self.switch_screen(controller, StartPage))
        button2 = tk.Button(self, text="Visit Page 1",
                            command=lambda: self.switch_screen(controller, PageOne))
        button1.place(relx=0.25, rely=0.85, anchor=tk.CENTER)
        button2.place(relx=0.75, rely=0.85, anchor=tk.CENTER)

    def show_screen(self):
        print("Two")
        
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.video_loop, args=(), daemon=True)
        self.thread.start()

    def switch_screen(self, controller, screen):
        self.on_close()
        controller.show_frame(screen)

    n = 0
        
    def video_loop(self):
        # DISCLAIMER:
        # I'm not a GUI developer, nor do I even pretend to be. This
        # try/except statement is a pretty ugly hack to get around
        # a RunTime error that Tkinter throws due to threading
        try:
            print(self.stop_event.is_set())
            # keep looping over frames until we are instructed to stop
            while not self.stop_event.is_set():
                # print("do something: ", self.n)
                # self.n += 1

                # grab the frame from the video stream and resize it to
                # have a maximum width of 300 pixels
                self.frame = self.controller.vs.read()
                # self.frame = imutils.resize(self.frame, width=480)

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
                        self.switch_screen(self.controller, PageOne)
                        # self.root.current = 'result_screen'                     
                        # self.root.scan_screen.reset()
                    else:
                        self.frame_idx += 1

                else:
                    # Only process every n frame of video to save time
                    if self.frame_idx == self.FRAME_SKIPPING:
                        self.frame_idx = 0
                        _ = self.process_video(self.frame)
                    else:
                        self.frame_idx += 1

                self.display_video()
                
        except RuntimeError:
            print("[INFO] caught a RuntimeError")

    def on_close(self):
        # set the stop event, cleanup the camera, and allow the rest of
        # the quit process to continue
        self.n = 0
        print("[INFO] closing...")
        self.stop_event.set()
        print("[INFO] stop event set...")
        # self.thread.join()
        print("[INFO] join...")
        # self.vs.stop()

    def display_video(self):
        # OpenCV represents images in BGR order; however PIL
        # represents images in RGB order, so we need to swap
        # the channels, then convert to PIL and ImageTk format
        image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)

        # if the panel is not None, we need to initialize it
        if self.panel is None:
            self.panel = tk.Label(self, image=image)
            self.panel.image = image
            self.panel.pack()

        # otherwise, simply update the panel
        else:
            self.panel.configure(image=image)
            self.panel.image = image

    def process_video(self, frame):
        # Resize frame of video to 1/2 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=1/self.RESIZE_FACTOR, fy=1/self.RESIZE_FACTOR)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = small_frame[:, :, ::-1]

        # print("process!")
        clf_result = self.fr.recognize_face(rgb_frame, False)

        names, max_prob = clf_result

        # print("App: ", app)

        if (names is not None):
            print("-----")
            print("Name: ", names[0], " ", max_prob[0])

            # Open the door if name is not "Unknown" and prob > Threshold
            if (max_prob[0] > self.THRESHOLD):
                self.name = names[0]
                centroidX, centroidY = calc_centroid(self.fr.face_locations[0])
                
                centroidX *= self.RESIZE_FACTOR
                centroidY *= self.RESIZE_FACTOR

                top = centroidY - 100 if centroidY >= 100 else 0
                bottom = centroidY + 100 if centroidY < frame.shape[1] else frame.shape[1]
                left = centroidX - 100 if centroidX >= 100 else 0
                right = centroidX + 100 if centroidX < frame.shape[0] else frame.shape[0]

                crop_img = frame[top:bottom, left:right]
                # crop_texture = app.frame_to_texture(crop_img)

                # self.face_detected()
                self.frame_idx = 0
                self.frame_status = 'post'
                # self.root.result_screen.update_screen(self.name, max_prob[0], crop_texture)
                
            print("-----")

        return clf_result


app = App()
app.geometry("800x480")
app.mainloop()
