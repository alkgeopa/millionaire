from __future__ import annotations

from tkinter import Frame, Label
from typing import TYPE_CHECKING

from constants import AMOUNTS
from widgets import *

if TYPE_CHECKING:
    from controller import LifelineController


class SidePanelFrame(Frame):
    """Based on the tkinter frame. Acts as a container for the lifeline and the amount widgets"""

    def __init__(self, master: Misc | None = ..., controller: LifelineController | None = ..., **kw) -> None:
        super().__init__(master=master, **kw)
        self.lifelineController = controller
        self.gameController = controller.gameController
        self.config(width=300, bg='black')
        self.pack(side='left', anchor='w', fill='y')

        # frame gia tis voitheies
        self.helps_frame = Frame(master=self, width=200, height=50, bg="black")
        self.helps_frame.grid(row=0, column=0)

        # Leitourgeikotita gia ta koumpia twn voitheiwn
        self.lifelines = [ALifelineButton] * 3
        for index, lifeline in enumerate(self.lifelineController.list):
            self.lifelines[index] = ALifelineButton(self.helps_frame, bg="black",
                                                    imgPath=resourcePath(f"img/{lifeline}.png"),
                                                    def_adress=self.lifelineController.lifelineHandler, text=lifeline)
            self.lifelines[index].grid(row=0, column=index)

        # frame gia ta posa
        self.posa_frame = Frame(master=self, width=260, height=555, bg="black")
        self.posa_frame.grid(row=3, column=0)

        self.posa = []
        for i in range(15, 0, -1):
            self.button = Label(self.posa_frame, bg="black", fg="#ffb51e", font=('san-serif', 12, 'bold'),
                                text=str(i) + "." + " " + str(AMOUNTS[i - 1]['string']),
                                width=35, pady=8)
            if i == 15 or i == 10 or i == 5:
                self.button.config(font=('san-serif', 14, 'bold'))
            self.posa.append(self.button)

        for i in range(len(self.posa)):
            self.posa[i].grid(row=i, column=0)

        self.highlightCurrentAmmount(self.gameController.level)

    def highlightCurrentAmmount(self, index) -> None:
        """Colors the current question/amount"""
        self.posa[14 - index].config(foreground='black', background='#ffb51e')
