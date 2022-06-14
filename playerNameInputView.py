from __future__ import annotations

from tkinter import Misc, Frame, Label, Entry, Button
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controller import PlayerNameController


class PlayerNameInputView(Frame):
    """View & container for the player name input related widgets"""

    def __init__(self, master: Misc | None = ..., controller: PlayerNameController | None = ..., **kw) -> None:
        super().__init__(master=master, **kw)
        self.controller = controller
        self.place(relx=0.5, rely=0.5, anchor='center')
        self['bg'] = 'black'
        self.message = Label(self, text='Enter your name')
        self.message.config(bg='black', fg='white', font=('Arial', 15, 'bold'))
        self.message.pack(pady=20)
        self.playerNameEntry = Entry(self, textvariable=self.controller.playerName)
        self.playerNameEntry.config(bg='black', fg='aqua', highlightthickness=2, highlightcolor='aqua',
                                    highlightbackground='white', insertbackground='aqua', font=('Arial', 20, 'bold'),
                                    justify='center')
        self.playerNameEntry.unbind_all('<Return>')
        self.playerNameEntry.focus_set()
        self.playerNameEntry.pack()
        self.startButton = Button(self, text='Start Game', command=self.startGame())
        self.startButton.config(bg='aqua', fg='black', highlightthickness=0, highlightcolor='aqua',
                                highlightbackground='white', relief='flat', activebackground='black',
                                activeforeground='aqua', font=('Arial', 20, 'bold'), justify='center')
        self.startButton.pack(pady=20)

    def startGame(self):
        return self.controller.startHandler
