import time
import hashlib

import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image
from PIL import ImageTk
import cv2

from doorlock.constants import LARGE_FONT, MEDIUM_FONT

class AdminLoginScreen(tk.Frame):
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        self.title_txt = tk.StringVar()
        self.subtitle_txt = tk.StringVar()

        display_container = tk.Frame(self, bg="#2026A1")
        form_container = tk.Frame(self, bg="#FFFFFF", height=10)
        display_container.pack(side=tk.LEFT, fill="both", expand=True)
        form_container.pack(side=tk.RIGHT, fill="both")

        self.title = tk.Label(display_container, textvariable=self.title_txt, font=LARGE_FONT)
        self.subtitle = tk.Label(display_container, textvariable=self.subtitle_txt, font=MEDIUM_FONT)
        self.title.pack(pady=10, padx=10)
        self.subtitle.pack(pady=10, padx=10)
        
        username_lbl = tk.Label(form_container, text="Username")
        password_lbl = tk.Label(form_container, text="Password")
        self.username_form = tk.Entry(form_container)
        self.password_form = tk.Entry(form_container, show="*")
        
        username_lbl.pack()
        self.username_form.pack()
        password_lbl.pack()
        self.password_form.pack()

        self.update_info('Register User', 'Silahkan login dengan Admin terlebih dahulu')
        
        submit_btn = ttk.Button(form_container, text="Login", # style='W.TButton',
                            command=lambda: self.submit_click())
                            
        submit_btn.pack()

        self.app = app

    def submit_click(self):
        self.admin_account_check(self.username_form.get(), self.password_form.get())

    def show_screen(self):
        print("admin login")

    def admin_account_check(self, username, password):
        user_query = self.app.users_df[self.app.users_df.username == username]

        if (len(user_query) > 0):
            if (self.check_pwd(username, password)):
                if (user_query.is_admin.item()):
                    print("selamat, anda admin dengan account")
                    print("Username: " + username)
                    self.app.show_frame("registration")
                else:
                    self.update_info('Maaf', 'Anda bukan admin')
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
