import time
import hashlib
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image
from PIL import ImageTk

import pandas as pd
import cv2

from doorlock.constants import LARGE_FONT, MEDIUM_FONT, ASSETS_URL
from doorlock.styles import colors
from doorlock.textbox import TextBox


class RegistrationScreen(tk.Frame):
    def __init__(self, parent, app, users_df):
        tk.Frame.__init__(self, parent)
        self.title_txt = tk.StringVar()
        self.subtitle_txt = tk.StringVar()
        self.users_df = users_df
        self.app = app

        display_container = tk.Frame(self, bg=colors['navy'])
        form_container = tk.Frame(self, bg=colors['white'], height=10)
        display_container.pack(side=tk.LEFT, fill="both", expand=True)
        form_container.pack(side=tk.RIGHT, fill="both")

        self.title = ttk.Label(display_container, textvariable=self.title_txt, style='Display.TLabel')
        self.subtitle = ttk.Label(display_container, textvariable=self.subtitle_txt, style='Subtitle.TLabel')

        self.title.place(anchor=tk.SW, relx=0.075, rely=0.4)
        self.subtitle.place(anchor=tk.SW, relx=0.075, rely=0.45)

        image = Image.open(ASSETS_URL + 'img/register_img.png')
        self.img = ImageTk.PhotoImage(image)

        display_img = tk.Canvas(display_container, bg=colors['navy'], width=236, height=216, bd=0, highlightthickness=0, relief='ridge')
        display_img.place(relx=.5, rely=1, anchor=tk.S)
        display_img.create_image(118, 108, image=self.img)

        self.update_info('Register User', 'Silahkan login dengan Admin terlebih dahulu')
        
        username_lbl = tk.Label(form_container, text="Username", background=colors['white'])
        fullname_lbl = tk.Label(form_container, text="Nama Lengkap", background=colors['white'])
        password_lbl = tk.Label(form_container, text="Password", background=colors['white'])
        password_conf_lbl = tk.Label(form_container, text="Ulangi Password", background=colors['white'])
        self.username_form = TextBox(form_container, font=('Arial', 12), width=40)
        self.fullname_form = TextBox(form_container, font=('Arial', 12), width=40)
        self.password_form = TextBox(form_container, show="*", font=('Arial', 12), width=40)
        self.password_conf_form = TextBox(form_container, show="*", font=('Arial', 12), width=40)
        
        username_lbl.pack(padx=20, pady=(20, 0), anchor=tk.SW)
        self.username_form.pack(padx=20, pady=0)
        fullname_lbl.pack(padx=20, pady=(10, 0), anchor=tk.SW)
        self.fullname_form.pack(padx=20, pady=0)
        password_lbl.pack(padx=20, pady=(10, 0), anchor=tk.SW)
        self.password_form.pack(padx=20, pady=0)
        password_conf_lbl.pack(padx=20, pady=(10, 0), anchor=tk.SW)
        self.password_conf_form.pack(padx=20, pady=0)
        
        submit_btn = ttk.Button(form_container, text="Register", width=38, style='P.TButton',
                            command=lambda: self.submit_click())


        home_btn = ttk.Button(form_container, text="Back to Home", width=38, # style='W.TButton',
                            command=lambda: app.show_frame("home"))
                            
        submit_btn.pack(padx=20, pady=(20, 0))
        home_btn.pack(padx=20, pady=(10, 0))

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
