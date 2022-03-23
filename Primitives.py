from tkinter import *


class AHoverButton(Button):
    def __init__(self, master, **kw) -> None:
        super().__init__(master=master, **kw)
        self.defaultBackground = self['background']
        self.defaultForeground = self['foreground']
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']
        self['foreground'] = self['activeforeground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground
        self['foreground'] = self.defaultForeground

