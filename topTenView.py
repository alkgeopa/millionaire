from __future__ import annotations

from tkinter import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controller import TopTenController


class TopTenView(Frame):
    """View for the list of the 10 best players. Displays the data provided by the database API"""

    def __init__(self, master: Misc | None = ..., controller: TopTenController | None = ..., **kw):
        super().__init__(master=master, **kw)
        self.controller = controller
        self.place(relx=0.5, rely=0, anchor=N)
        self.config(bg='purple', padx=20, pady=40)
        self.backToMenuButton = Button(self, text='Back to menu', command=self.controller.mainMenuView)
        self.backToMenuButton.pack(side='bottom', anchor='s', pady=(40, 0))
        self.title = Label(self, text='TOP 10 PLAYERS', font=('san-serif', 30, 'bold'), bg='purple', fg='white')
        self.title.pack()

        # container for the player statistics
        self.playersList = Frame(self)
        self.playersList.pack()

        # column labels
        self.headings: list[Label] = []
        self.headings.append(Label(self.playersList, text="Name"))
        self.headings.append(Label(self.playersList, text="Amount Won"))
        self.headings.append(Label(self.playersList, text="Total Time"))
        self.headings.append(Label(self.playersList, text="Av. Question Time"))
        self.headings.append(Label(self.playersList, text="Score"))
        for col, heading in enumerate(self.headings):
            heading.config(font=('san-serif', 12, 'bold'))
            heading.grid(row=0, column=col, padx=10)

        # the actual list of statistics
        for row, players in enumerate(self.controller.playersInfo):
            Label(self.playersList, text=str(players.get("name"))).grid(row=row + 1, column=0)
            Label(self.playersList, text=str(players.get("amountWon"))).grid(row=row + 1, column=1)
            Label(self.playersList, text=str(players.get("totalTime"))).grid(row=row + 1, column=2)
            Label(self.playersList, text=str(players.get("averageQuestionTime"))).grid(row=row + 1, column=3)
            Label(self.playersList, text=str(players.get("score"))).grid(row=row + 1, column=4)
