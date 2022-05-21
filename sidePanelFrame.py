from widgets import *
from typing import TYPE_CHECKING
from constants import LIFELINES, AMOUNTS

if TYPE_CHECKING:
    from controller import LifelineController


class SidePanelFrame(Frame):
    def __init__(self, master: Misc | None = ..., controller: 'LifelineController' = None, **kw) -> None:
        super().__init__(master=master, **kw)
        self.lifelineController = controller
        self.gameController = controller.gameController
        self["width"] = 400
        self.pack(side=LEFT, anchor=W)
        # # Τα ποσά καλό θα ήταν να μπουν σε λίστα από Labels
        #
        # # Για τα κουμπιά των βοηθειών χρησιμοποιούμε ALifelineButton αντί για Button

        # # Καλό είναι, τα ποσά να είναι σε μέσα σε ένα Frame και οι βοήθειες μέσα σε ένα άλλο Frame
        #
        # Από εδώ αρχίζουμε να γράφουμε
        self["background"] = "black"

        self.lifelinesFrame = Frame(self, bg="black")
        self.lifelinesFrame.pack(side=TOP, anchor=N)
        self.lifelines = [ALifelineButton] * len(LIFELINES)
        for index, lifeline in enumerate(self.lifelineController.lifelinesInfo.keys()):
            self.lifelines[index] = ALifelineButton(
                self.lifelinesFrame,
                f"./img/{lifeline}.png",
                text=lifeline,
                callback=self.lifelineController.lifelineHandler,
            )
            self.lifelines[index].resizeButtonImage(ANSWERWIDTH, ANSWERHEIGHT)
            self.lifelines[index].grid(row=0, column=index, padx=10)
            self.lifelineController.lifelinesInfo[lifeline] = self.lifelines[
                index
            ]  # TODO

        self.amountsFrame = Frame(self, bg="black")
        self.amountsFrame.pack(pady=20)
        self.amounts = [Label] * len(AMOUNTS)
        for index, amount in enumerate(AMOUNTS):
            if amount == '1.000' or amount == '7.500':
                self.amounts[index] = Label(
                    self.amountsFrame,
                    width=25,
                    pady=1,
                    font="Arial 20 bold underline",
                    foreground="grey",
                    background="black",
                    text=f"{str(index + 1)}   {amount} €",
                )
            else:
                self.amounts[index] = Label(
                    self.amountsFrame,
                    width=25,
                    pady=1,
                    font="Arial 20 bold",
                    foreground="grey",
                    background="black",
                    text=f"{str(index + 1)}   {amount} €",
                )
            self.amounts[index].pack(side=BOTTOM, anchor=S)
        self.highlightCurrentAmmount(self.gameController.level)

    def highlightCurrentAmmount(self, index) -> None:
        self.amounts[index].config(foreground='black', background='#ffb51e')
