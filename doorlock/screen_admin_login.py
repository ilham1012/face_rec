import time
import hashlib

import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image
from PIL import ImageTk
import cv2

from doorlock.screen_login import LoginScreen
from doorlock.constants import LARGE_FONT, MEDIUM_FONT, ASSETS_URL
from doorlock.styles import colors

class AdminLoginScreen(LoginScreen):
    # def __init__(self, parent, app):
    #     pass

    def account_check(self, username, password):
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