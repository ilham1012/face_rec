import time
import hashlib

import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image
from PIL import ImageTk
import cv2

from doorlock.constants import LARGE_FONT, MEDIUM_FONT, ASSETS_URL
from doorlock.styles import colors
from doorlock.textbox import TextBox

class LoginScreen(tk.Frame):
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        self.title_txt = tk.StringVar()
        self.subtitle_txt = tk.StringVar()

        display_container = tk.Frame(self, bg=colors['navy'])
        form_container = tk.Frame(self, bg=colors['white'])
        display_container.pack(side=tk.LEFT, fill="both", expand=True)
        form_container.pack(side=tk.RIGHT, fill="both")

        self.title = ttk.Label(display_container, textvariable=self.title_txt, style='Display.TLabel')
        self.subtitle = ttk.Label(display_container, textvariable=self.subtitle_txt, style='Subtitle.TLabel')

        self.title.place(anchor=tk.SW, relx=0.075, rely=0.4)
        self.subtitle.place(anchor=tk.SW, relx=0.075, rely=0.45)

        image = Image.open(ASSETS_URL + 'img/register_img.png')
        self.img = ImageTk.PhotoImage(image)

        display_img = tk.Canvas(display_container, bg=colors['navy'], width=400, height=216, bd=0, highlightthickness=0, relief='ridge')
        display_img.place(relx=.5, rely=1, anchor=tk.S)
        display_img.create_image(200, 108, image=self.img)

        self.update_info('Register User', 'Silahkan login dengan Admin terlebih dahulu')
        
        username_lbl = tk.Label(form_container, text="Username", background=colors['white'])
        password_lbl = tk.Label(form_container, text="Password", background=colors['white'])
        self.username_form = TextBox(form_container, font=('Arial', 12), width=40)
        self.password_form = TextBox(form_container, show="*", font=('Arial', 12), width=40)
        
        username_lbl.pack(padx=20, pady=(20,0), anchor=tk.SW)
        self.username_form.pack(padx=20, pady=0)
        password_lbl.pack(padx=20, pady=(10,0), anchor=tk.SW)
        self.password_form.pack(padx=20, pady=0)

        
        submit_btn = ttk.Button(form_container, text="Login", width=38, style='P.TButton',
                            command=lambda: self.submit_click())
                            
        home_btn = ttk.Button(form_container, text="Back to Home", width=38,
                            command=lambda: app.show_frame("home"))
                            
        submit_btn.pack(padx=20, pady=(20, 0))
        home_btn.pack(padx=20, pady=(10, 0))

        self.app = app

    def submit_click(self):
        self.account_check(self.username_form.get(), self.password_form.get())
        self.reset_form()

    def show_screen(self):
        print("[SHOW SCREEN] Login")

    def account_check(self, username, password):
        user_query = self.app.users_df[self.app.users_df.username == username]

        if (len(user_query) > 0):
            if (self.check_pwd(username, password)):
                print("selamat Datang")
                print("Username: " + username)
                self.app.result_screen.update_info(username, 0, mode=1)
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

    def reset_form(self):
        self.username_form.delete(0, tk.END)
        self.password_form.delete(0, tk.END)

    def check_pwd(self, username, pwd):
        ret = False
        md5_pwd = hashlib.md5(pwd.encode()).hexdigest()
        if (md5_pwd == self.app.users_df[self.app.users_df.username == username].password.item()):
            ret = True
        return ret
