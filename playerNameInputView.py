from __future__ import annotations

from tkinter import Button, Entry, Frame, Label, Misc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controller import GameController


class PlayerNameInputView(Frame):
    def __init__(self, master: Misc | None = ..., controller: type[GameController] = ..., **kw) -> None:
        super().__init__(master=master, **kw)
        self.controller = controller
        self.place(relx=0.5, rely=0.5, anchor='center')
        self.message = Label(self, text='Enter your name')
        self.message.pack(pady=20)
        self.playerNameEntry = Entry(self, textvariable=self.controller.playerName)
        self.playerNameEntry.pack()
        self.startButton = Button(self, text='Start Game', command=self.startGame())
        self.startButton.pack(pady=20)

    def startGame(self):
        return self.controller.playerNameStartHandler
