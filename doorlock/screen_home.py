import time
# from os import system

import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
# import RPi.GPIO as GPIO

from doorlock.constants import LARGE_FONT, MEDIUM_FONT, ASSETS_URL
from doorlock.styles import colors

class HomeScreen(tk.Frame):
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        self.app = app

        display_container = tk.Frame(self, bg=colors['navy'])
        button_container = tk.Frame(self, bg=colors['white'], height=10)
        display_container.pack(side=tk.TOP, fill="both", expand=True)
        button_container.pack(side=tk.BOTTOM, fill="both")

        label_title = ttk.Label(display_container, style='Display.TLabel', text="Halo!")
        label_subtitle = ttk.Label(display_container, style='Subtitle.TLabel', text="Saat ini ada 3 orang di Lab")

        label_title.place(relx=0.075, rely=0.55, anchor=tk.SW)
        label_subtitle.place(relx=0.075, rely=0.6, anchor=tk.SW)

        image = Image.open(ASSETS_URL + 'img/home_img.png')
        self.img = ImageTk.PhotoImage(image)

        home_img = tk.Canvas(display_container, bg=colors['navy'], width=363, height=250, bd=0, highlightthickness=0, relief='ridge')
        home_img.place(relx=.95, rely=.95, anchor=tk.SE)
        home_img.create_image(181, 125, image=self.img)

        hamburger_img = Image.open(ASSETS_URL + 'img/hamburger.png')
        self.menu_img = ImageTk.PhotoImage(hamburger_img)

        button1 = ttk.Button(button_container, text="Bunyikan Bel", style='TButton',
                            command=lambda: self.ring_the_bell())
        button2 = ttk.Button(button_container, text="Masuk", style='P.TButton',
                            command=lambda: app.show_frame("scan"))
        button3 = ttk.Button(display_container, image=self.menu_img, style='S.TButton',
                            command=lambda: app.show_frame("admin_login"))
        
        button1.configure()
        button2.configure()
        button3.configure()

        button1.pack(side=tk.LEFT, pady=30, padx=50, fill=tk.BOTH, expand=True)
        button2.pack(side=tk.LEFT, pady=30, padx=50, fill=tk.BOTH, expand=True)

        button3.place(relx=0.05, rely=0.05, anchor=tk.NW)

    def show_screen(self):
        print("[SHOW SCREEN] Home")

    def ring_the_bell(self):
        print("[BELL] RIIIIING!")
        # sound_file = ASSETS_URL + 'sounds/doorbell.mp3'
        # system("mpg123 " + sound_file)
        i = 0
        pitch = [82, 65]
        duration = [0.2, 0.4]

        for p in pitch:
            self.buzzer(p, duration[i])
            time.sleep(duration[i] * 0.5)
            x+=1

    buzzer_pin = 18
    # from http://andidinata.com/2017/10/music-dengan-piezo-buzzer/
    def buzzer(self, pitch, duration):
        if(pitch==0):
            time.sleep(duration)
            return

        period = 1.0/pitch
        delay=period/2
        cycles=int(duration*pitch)

        for i in range(cycles):
            self.app.GPIO.output(self.buzzer_pin,1)
            time.sleep(delay)
            self.app.GPIO.output(self.buzzer_pin,0)
            time.sleep(delay)

    def GPIO_init(self):
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(self.buzzer_pin, GPIO.OUT, initial=0)
        pass