from __future__ import annotations

from tkinter import Misc, Frame, Label, Button
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controller import GameController


class ResultView(Frame):
    """Base class for the victory/defeat frames"""

    def __init__(self, master: Misc | None = ..., controller: GameController | None = ..., **kw) -> None:
        super().__init__(master, **kw)
        self.gameController = controller

        self.pack(side='right', anchor='e', expand=1, fill='both')

        self.messageFrame = Frame(master=self)
        self.messageFrame.place(relx=0.5, rely=0.5, anchor='center')

        self.title = Label(master=self.messageFrame, text='', justify='center')

        self.amountWon = Label(master=self.messageFrame, justify='center')

        self.level = Label(master=self.messageFrame, justify='center')

        self.button = Button(master=self.messageFrame, text='OK', relief='flat',
                             command=self.gameController.appController.setMainMenuController)


class DefeatView(ResultView):
    """Frame for when the player loses"""

    def __init__(self, master: Misc | None = ..., controller: GameController | None = ..., **kw) -> None:
        super().__init__(master=master, controller=controller, **kw)
        self.config(bg='brown')
        self.messageFrame.config(bg='brown')
        self.title.config(text='Δυστυχώς χάσατε!\nΠροσπαθήστε ξανά.', font=('san-serif', 20, 'bold'), bg='brown')
        self.title.pack(side='top', anchor='n')
        self.button.config(bg='white', width=5)
        self.button.pack(side='top', anchor='n')


class SafetyNetView(ResultView):
    """Frame for when the player falls to the safety net"""

    def __init__(self, master: Misc | None = ..., controller: GameController | None = ..., **kw) -> None:
        super().__init__(master=master, controller=controller, **kw)
        self.config(bg='lime')
        self.messageFrame.config(bg='lime')
        self.title.config(text=f'Κερδίσατε το μαξιλαράκι των', bg='lime', font=('san-serif', 15, 'bold'))
        self.title.pack(side='top', anchor='n')
        self.amountWon.config(text=f"{self.gameController.amountWon}€", bg='lime', font=('san-serif', 20, 'bold'))
        self.amountWon.pack(side='top', anchor='n')
        self.button.config(bg='white', width=5)
        self.button.pack(side='top', anchor='n')


class MillionaireView(ResultView):
    """Frame for when the player wins the game"""

    def __init__(self, master: Misc | None = ..., controller: GameController | None = ..., **kw) -> None:
        super().__init__(master=master, controller=controller, **kw)
        self.config(bg='white')
        self.messageFrame.config(bg='white')
        self.title.config(text='ΣΥΓΧΑΡΗΤΗΡΙΑ!\nΚΕΡΔΙΣΑΤΕ ΤΟ ΠΑΙΧΝΙΔΙ!', bg='white', font=('san-serif', 20, 'bold'))
        self.title.pack(side='top', anchor='n')
        self.amountWon.config(text=self.gameController.amountWon, bg='white')
        self.amountWon.pack(side='top', anchor='n')
        self.button.config(bg='green', width=5)
        self.button.pack(side='top', anchor='n')
