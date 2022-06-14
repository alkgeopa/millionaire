from __future__ import annotations

from tkinter import Button, Label
from typing import TYPE_CHECKING

from view import *

if TYPE_CHECKING:
    from controller import GameController


class GameView(AView):
    """The game view. All widget concerning the game are placed in this view"""

    def __init__(self, master: Misc | None = ..., controller: GameController | None = None, **kw) -> None:
        super().__init__(master, **kw)
        self.controller = controller
        self["bg"] = "black"
        self.pack(expand=1, fill='both')

        # info bar at the bottom of the view
        self.infoFrame = Frame(self, bg='black')
        self.infoFrame.pack(side='bottom', anchor='s', fill='x')
        # button to
        self.backToMenuButton = Button(self.infoFrame, text='Back to menu', bg='black', fg='white')
        self.backToMenuButton.pack(side='right', anchor='e')

        self.infoBarTitle = Label(self.infoFrame, text='ΠΟΙΟΣ ΘΕΛΕΙ ΝΑ ΓΙΝΕΙ ΕΚΑΤΟΜΜΥΡΙΟΥΧΟΣ', bg='black', fg='gray')
        self.infoBarTitle.pack(side='bottom', anchor='s')
