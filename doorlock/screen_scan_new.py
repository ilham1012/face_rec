import threading

from PIL import Image
from PIL import ImageTk
import tkinter as tk
import imutils
from imutils.video import VideoStream
import cv2

from utils.util import calc_centroid
from doorlock.register_face import RegisterFace
from doorlock.constants import LARGE_FONT, MEDIUM_FONT

class ScanNewScreen(tk.Frame):
    frame_status = "pre" # ['pre', 'on', 'post']
    frame_idx = 0
    name = ""

    # Const
    PRE_FRAME = 90
    POST_FRAME = 135
    FRAME_SKIPPING = 30

    THRESHOLD = 0.85
    RESIZE_FACTOR = 4

    def __init__(self, parent, app, users_df):
        tk.Frame.__init__(self, parent)
        self.frame = None
        self.thread = None
        self.stopEvent = None
        self.app = app
        self.rf = RegisterFace(users_df)

        self.panel = tk.Label(self)
        self.panel.place(relx=0.5, rely=0, anchor=tk.N)

        label = tk.Label(self, text="Page Two", font=LARGE_FONT)
        label.place()

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: self.switch_screen("home"))

        button1.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    def show_screen(self):
        print("[SHOW SCREEN] Scan New Face")
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.video_loop, args=(), daemon=True)
        self.thread.start()

    def switch_screen(self, screen):
        self.on_close()
        # app.result_screen.update_text(self.name)
        self.app.show_frame(screen)
        
    def video_loop(self):
        # DISCLAIMER:
        # I'm not a GUI developer, nor do I even pretend to be. This
        # try/except statement is a pretty ugly hack to get around
        # a RunTime error that Tkinter throws due to threading
        try:
            print(self.stop_event.is_set())
            # keep looping over frames until we are instructed to stop
            while not self.stop_event.is_set():
                # grab the frame from the video stream and resize it to
                # have a maximum width of 300 pixels
                self.frame = self.app.video_stream.read()
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
                        self.switch_screen("home")
                        # self.root.current = 'result_screen'                     
                        # self.root.scan_screen.reset()
                    else:
                        self.frame_idx += 1

                else:
                    # Only process every n frame of video to save time
                    if self.frame_idx == self.FRAME_SKIPPING:
                        self.frame_idx = 0
                        self.process_video(self.frame)
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
            self.panel.place()

        # otherwise, simply update the panel
        else:
            self.panel.configure(image=image)
            self.panel.image = image

    def process_video(self, frame):
        # Resize frame of video to 1/2 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=1/self.RESIZE_FACTOR, fy=1/self.RESIZE_FACTOR)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = small_frame[:, :, ::-1]

        if (len(self.rf.face_encodings) < self.rf.NEW_DATA):
            self.rf.capture_face(rgb_frame)
        else:
            train_success = self.rf.data_prep()
            if (train_success):
                # break
                self.frame_idx = 0
                self.frame_status = 'post'
                self.app.scan_screen.fr.load_model()
