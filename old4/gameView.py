from view import *


class GameView(AView):
    def __init__(self, master: Misc | None = ..., controller=None, **kw) -> None:
        super().__init__(master, **kw)
        self.controller = controller
        self["bg"] = "black"
        self.pack(expand=1, fill=BOTH)

