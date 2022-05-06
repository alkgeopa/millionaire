from tkinter import *

class AView(Frame):
    def __init__(self, master: Misc | None = ..., **kw) -> None:
        super().__init__(master, **kw)

    @classmethod
    def fromFrame(cls):
        ...
