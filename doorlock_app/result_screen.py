import time

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen

class ResultScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.display_screen)

    def display_screen(self, dt):
        app = App.get_running_app()
        print('sleep')
        time.sleep(5)
        print('wakeup')
        print(app.root.current)
        app.root.current = 'front_screen'

    def update_screen(self, name, score, crop_texture):
        if (name != "unknown"):
            txt1 = "Wajah dikenali"
            txt2 = "Selamat Datang"
            self.open_door()
        else:
            txt1 = "Wajah terdeteksi"
            txt2 = "Maaf Anda Tidak Terdaftar"

        txt3 = name.capitalize()
        txt4 = "Confidence score: {:2.0f}%".format(score*100)

        self.ids.img_display.ids.crop_img.texture = crop_texture
        self.ids.info_text.text = txt1
        self.ids.info_text_2.text = txt2
        self.ids.info_text_3.text = txt3
        self.ids.info_text_4.text = txt4

    def open_door(self):
        print("OPEN THE DOOR")
        # result = firebase.put_async(device_url, 'lock', False, callback=relock)
        # result = firebase.put(device_url, 'lock', False)
        # relock(result)