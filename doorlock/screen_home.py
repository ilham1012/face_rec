import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk

from doorlock.constants import LARGE_FONT, MEDIUM_FONT, ASSETS_URL
from doorlock.styles import colors

class HomeScreen(tk.Frame):
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)

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

        button1 = ttk.Button(button_container, text="Daftar", style='TButton',
                            command=lambda: app.show_frame("admin_login"))
        button2 = ttk.Button(button_container, text="Masuk", style='P.TButton',
                            command=lambda: app.show_frame("scan"))
        
        button1.configure()
        button2.configure()
        button1.pack(side=tk.LEFT, pady=30, padx=50, fill=tk.BOTH, expand=True)
        button2.pack(side=tk.LEFT, pady=30, padx=50, fill=tk.BOTH, expand=True)

    def show_screen(self):
        print("[SHOW SCREEN] Home")
