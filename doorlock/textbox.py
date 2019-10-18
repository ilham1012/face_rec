import subprocess

import tkinter.ttk as ttk

class TextBox(ttk.Entry):
    def __init__(self, master=None, widget=None, **kw):
        super().__init__(master, widget, **kw)
        self.bind('<FocusIn>', self.focus_in)
        self.bind('<FocusOut>', self.focus_out)

    def focus_out(self, event):
        print("[TextBox] Focus Out")
        subprocess.Popen(["pkill", "onboard"])

    def focus_in(self, event):
        print("[TextBox] Focus In")
        subprocess.Popen("onboard")
