from __future__ import annotations

from tkinter import Frame, Label
from typing import TYPE_CHECKING
from widgets import AMenuButton

if TYPE_CHECKING:
    from main import MainWindow


class MenuLevel:
    def __init__(self, root: MainWindow) -> None:
        self.windowRoot = root

        self.menuLevel = Frame(self.windowRoot, bg='black')
        self.menuLevel.place(relx=0.5, rely=0.5, anchor='center')

        self.title = Label(self.menuLevel, text='ΠΟΙΟΣ ΘΕΛΕΙ ΝΑ ΓΙΝΕΙ ΕΚΑΤΟΜΜΥΡΙΟΥΧΟΣ',
                           font=('san-serif', 40, 'bold'), bg='black', fg='white', wraplength=600)
        self.title.pack()

        self.btnStart = AMenuButton(master=self.menuLevel, text='Start', font=(
            'san-serif', 20, 'bold'), width=10, height=1, command=self.startHandler)
        self.btnStart.pack(pady=20)
        self.btnTopTen = AMenuButton(master=self.menuLevel, text='Top 10', font=(
            'san-serif', 20, 'bold'), width=10, height=1, command=self.topTenHandler)
        self.btnTopTen.pack(pady=20)
        self.btnExit = AMenuButton(
            master=self.menuLevel, text='Exit', font=('san-serif', 20, 'bold'),
            width=10, height=1, command=self.windowRoot.quit)
        self.btnExit.pack(pady=20)

    def startHandler(self):
        self.windowRoot.changeLevel('GameLevel')

    def topTenHandler(self):
        ...

    def destroy(self):
        self.menuLevel.destroy()
