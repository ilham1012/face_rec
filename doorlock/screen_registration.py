import time
import hashlib
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image
from PIL import ImageTk

import pandas as pd
import cv2

from doorlock.constants import LARGE_FONT, MEDIUM_FONT

class RegistrationScreen(tk.Frame):
    def __init__(self, parent, app, users_df):
        tk.Frame.__init__(self, parent)
        self.title_txt = tk.StringVar()
        self.subtitle_txt = tk.StringVar()
        self.users_df = users_df
        self.app = app

        display_container = tk.Frame(self, bg="#2026A1")
        form_container = tk.Frame(self, bg="#FFFFFF", height=10)
        display_container.pack(side=tk.LEFT, fill="both", expand=True)
        form_container.pack(side=tk.RIGHT, fill="both")

        self.title = tk.Label(display_container, textvariable=self.title_txt, font=LARGE_FONT)
        self.subtitle = tk.Label(display_container, textvariable=self.subtitle_txt, font=MEDIUM_FONT)
        self.title.pack(pady=10, padx=10)
        self.subtitle.pack(pady=10, padx=10)
        
        username_lbl = tk.Label(form_container, text="Username")
        fullname_lbl = tk.Label(form_container, text="Nama Lengkap")
        password_lbl = tk.Label(form_container, text="Password")
        password_conf_lbl = tk.Label(form_container, text="Ulangi Password")
        self.username_form = tk.Entry(form_container)
        self.fullname_form = tk.Entry(form_container)
        self.password_form = tk.Entry(form_container, show="*")
        self.password_conf_form = tk.Entry(form_container, show="*")
        
        username_lbl.pack()
        self.username_form.pack()
        fullname_lbl.pack()
        self.fullname_form.pack()
        password_lbl.pack()
        self.password_form.pack()
        password_conf_lbl.pack()
        self.password_conf_form.pack()
        
        submit_btn = ttk.Button(form_container, text="Register", # style='W.TButton',
                            command=lambda: self.submit_click())


        home_btn = ttk.Button(form_container, text="Back to Home", # style='W.TButton',
                            command=lambda: app.show_frame("home"))
                            
        submit_btn.pack()
        home_btn.pack()

        self.update_info('Register User', 'Silahkan masukkan profile anda.')

        self.app = app

    def submit_click(self):
        username = self.username_form.get()
        fullname = self.fullname_form.get()
        password = self.password_form.get()
        password_conf = self.password_conf_form.get()

        if (password == password_conf):
            if (self.check_username_exist(username)):
                self.update_info("Maaf", "Username " + username + " sudah ada. Mohon untuk menggantinya.")
            else:
                user = self.create_user(username, fullname, password)
                print(user)
                print("capture face")
                self.app.scan_new_screen.rf.set_data(user)
                self.app.show_frame("scan_new")
                
        else:
            self.update_info("Maaf", "Konfirmasi Password tidak sama")

    def show_screen(self):
        print("registration")

    def update_info(self, title_text, subtitle_text):
        txt_title = title_text.capitalize()
        txt_subtitle = subtitle_text

        self.title_txt.set(txt_title)
        self.subtitle_txt.set(txt_subtitle)

    def create_user(self, username, name, pwd):
        md5_pwd = hashlib.md5(pwd.encode()).hexdigest()
        row = [[username, name, md5_pwd, False]]
        new_user = pd.DataFrame(row, columns=['username', 'full_name', 'password', 'is_admin'])
        return new_user

    def check_username_exist(self, username):
        ret = False
        user_query = self.users_df[self.users_df.username == username]
        if(len(user_query) > 0):
            ret = True
            if (len(user_query) > 1):
                print("Something's wrong here!")
                print(user_query)
        return ret
