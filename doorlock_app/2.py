from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import tkinter as tk
import threading
import datetime
import imutils
from imutils.video import VideoStream
import cv2
import os
import time

import face_recognition

LARGE_FONT = ("Verdana", 12)


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.vs = VideoStream(usePiCamera=False).start()
        

        root_frame = tk.Frame(self)

        root_frame.pack(side="top", fill="both", expand=True)

        root_frame.grid_rowconfigure(0, weight=1)
        root_frame.grid_columnconfigure(0, weight=1)

        self.screens = {}

        page_start = StartPage(root_frame, self)
        self.screens[StartPage] = page_start
        page_start.grid(row=0, column=0, sticky="nsew")

        page_one = PageOne(root_frame, self)
        self.screens[PageOne] = page_one
        page_one.grid(row=0, column=0, sticky="nsew")

        page_two = PageTwo(root_frame, self)
        self.screens[PageTwo] = page_two
        page_two.grid(row=0, column=0, sticky="nsew")

        print(self.screens)
        self.show_frame(StartPage)
        self.wm_protocol("WM_DELETE_WINDOW", self.on_close)
        

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
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(PageOne))
        button2 = tk.Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(PageTwo))
        button1.pack()
        button2.pack()

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
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.vs = None
        self.frame = None
        self.thread = None
        self.stopEvent = None
        self.controller = controller

        self.panel = tk.Label(self)
        self.panel.pack(padx=10, pady=10)

        label = tk.Label(self, text="Page Two", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: self.switch_screen(controller, StartPage))
        button2 = tk.Button(self, text="Visit Page 1",
                            command=lambda: self.switch_screen(controller, PageOne))
        button1.pack()
        button2.pack()

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
                print("do something: ", self.n)
                self.n += 1

                # grab the frame from the video stream and resize it to
                # have a maximum width of 300 pixels
                self.frame = self.controller.vs.read()
                self.frame = imutils.resize(self.frame, width=300)

                
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
                    self.panel.pack(padx=10, pady=10)
		
                # otherwise, simply update the panel
                else:
                    self.panel.configure(image=image)
                    self.panel.image = image
 
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




app = App()
app.geometry("800x600")
app.mainloop()
