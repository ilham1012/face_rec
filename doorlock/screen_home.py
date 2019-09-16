import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk

from doorlock.constants import LARGE_FONT, MEDIUM_FONT, ASSETS_URL


class HomeScreen(tk.Frame):
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)

        display_container = tk.Frame(self, bg="#2026A1")
        button_container = tk.Frame(self, bg="#FFFFFF", height=10)
        display_container.pack(side=tk.TOP, fill="both", expand=True)
        button_container.pack(side=tk.BOTTOM, fill="both")

        label = tk.Label(display_container, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        image = Image.open(ASSETS_URL + 'img/home_img.png')
        self.img = ImageTk.PhotoImage(image)

        home_img = tk.Canvas(display_container, bg="#2026A1", width=363, height=250, bd=0, highlightthickness=0, relief='ridge')
        home_img.pack()
        home_img.create_image(181, 125, image=self.img)

        style = ttk.Style()
        style.configure('W.TButton', font=('Arial', 10, 'bold'), background='#2026A1', foreground='white')

        button1 = ttk.Button(button_container, text="Visit Page 1", style='W.TButton',
                            command=lambda: app.show_frame("admin_login")) #, width=1, height=1)
        button2 = ttk.Button(button_container, text="Visit Page 2", style='W.TButton',
                            command=lambda: app.show_frame("scan")) #, width=1, height=1)
        
        button1.configure() #font=MEDIUM_FONT)
        button2.configure() #font=MEDIUM_FONT)
        button1.pack(side=tk.LEFT, pady=30, padx=50, fill=tk.BOTH, expand=True)
        button2.pack(side=tk.LEFT, pady=30, padx=50, fill=tk.BOTH, expand=True)

    def show_screen(self):
        print("Home")