import time
import hashlib

import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image
from PIL import ImageTk
import cv2

from doorlock.constants import LARGE_FONT, MEDIUM_FONT, ASSETS_URL
from doorlock.styles import colors

class LoginScreen(tk.Frame):
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        self.title_txt = tk.StringVar()
        self.subtitle_txt = tk.StringVar()

        display_container = tk.Frame(self, bg="#2026A1")
        form_container = tk.Frame(self, bg="#FFFFFF")
        display_container.pack(side=tk.LEFT, fill="both", expand=True)
        form_container.pack(side=tk.RIGHT, fill="both")

        self.title = ttk.Label(display_container, textvariable=self.title_txt, style='Display.TLabel')
        self.subtitle = ttk.Label(display_container, textvariable=self.subtitle_txt, style='Subtitle.TLabel')

        self.title.place(anchor=tk.SW, relx=0.075, rely=0.4)
        self.subtitle.place(anchor=tk.SW, relx=0.075, rely=0.5)

        image = Image.open(ASSETS_URL + 'img/register_img.png')
        self.img = ImageTk.PhotoImage(image)

        display_img = tk.Canvas(display_container, bg=colors['navy'], width=400, height=216, bd=0, highlightthickness=0, relief='ridge')
        display_img.place(relx=.5, rely=1, anchor=tk.S)
        display_img.create_image(200, 108, image=self.img)

        self.update_info('Register User', 'Silahkan login dengan Admin terlebih dahulu')
        
        username_lbl = tk.Label(form_container, text="Username")
        password_lbl = tk.Label(form_container, text="Password")
        self.username_form = ttk.Entry(form_container, font=('Arial', 12), width=40)
        self.password_form = ttk.Entry(form_container, show="*", font=('Arial', 12), width=40)
        
        username_lbl.pack(padx=20, pady=(20,0), fill=tk.X)
        self.username_form.pack(padx=20, pady=10)
        password_lbl.pack(padx=20, pady=(10,0), fill=tk.X)
        self.password_form.pack(padx=20, pady=10)

        
        submit_btn = ttk.Button(form_container, text="Login", width=31, style='P.TButton',
                            command=lambda: self.submit_click())
                            
        home_btn = ttk.Button(form_container, text="Back to Home", width=31,
                            command=lambda: app.show_frame("home"))
                            
        submit_btn.pack(padx=20, pady=10)
        home_btn.pack(padx=20, pady=10)

        self.app = app

    def submit_click(self):
        self.account_check(self.username_form.get(), self.password_form.get())

    def show_screen(self):
        print("admin login")

    def account_check(self, username, password):
        user_query = self.app.users_df[self.app.users_df.username == username]

        if (len(user_query) > 0):
            if (self.check_pwd(username, password)):
                print("selamat Datang")
                print("Username: " + username)
                self.app.show_frame("result")
            else:
                self.update_info('Maaf', 'Username tidak terdaftar atau Password salah')
        else:
            self.update_info('Maaf', 'Username tidak terdaftar atau Password salah')

    def update_info(self, title_text, subtitle_text):
        txt_title = title_text.capitalize()
        txt_subtitle = subtitle_text

        self.title_txt.set(txt_title)
        self.subtitle_txt.set(txt_subtitle)

    def check_pwd(self, username, pwd):
        ret = False
        md5_pwd = hashlib.md5(pwd.encode()).hexdigest()
        if (md5_pwd == self.app.users_df[self.app.users_df.username == username].password.item()):
            ret = True
        return ret
