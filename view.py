from tkinter import Misc, Frame


class AView(Frame):
    """Base class equivalent to a tkinter Frame build with expandability in mind.
    All app views inherit this class"""

    def __init__(self, master: Misc | None = ..., **kw) -> None:
        super().__init__(master, **kw)
