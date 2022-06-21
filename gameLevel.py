from __future__ import annotations

from time import time
from tkinter import Frame, IntVar, Label, StringVar
from typing import TYPE_CHECKING

from constants import *
from widgets import *

if TYPE_CHECKING:
    from controller import GameController
    from main import MainWindow


class GameLevel(Frame):
    def __init__(self, root: MainWindow, controller: type[GameController], **kw) -> None:
        super().__init__(root, **kw)
        self.windowRoot = root
        self.pack()
        self.gameController = controller
        # Sidepanel-----------------------------------------------------------
        self.sideFrame = Frame(self.windowRoot, bg='black')
        self.sideFrame.pack(side='left', anchor='w', fill='y')
        # lifelines
        self.lifelineFrame = Frame(self.sideFrame, bg='black')
        self.lifelineFrame.pack(anchor='s', expand=1, fill='x', pady=20)
        self.lifelines = [ALifelineButton] * len(self.gameController.lifelines)
        for index, lifeline in enumerate(self.gameController.lifelines):
            self.lifelines[index] = ALifelineButton(
                self.lifelineFrame, imgPath=f'./img/{lifeline}.png', text=lifeline,
                callback=self.gameController.lifelineDispatch)
            self.lifelines[index].grid(row=0, column=index)
        # amounts
        self.amountFrame = Frame(self.sideFrame, bg='blue')
        self.amountFrame.pack(side='bottom', anchor='s')
        self.amounts: list[Label] = [Label] * len(AMOUNTS)
        for index, amount in enumerate(AMOUNTS):
            self.amounts[index] = Label(self.amountFrame, bg='black', fg='#ffb437', font=(
                'sans-serif', 16, 'bold'), justify='left', text=amount["string"], padx=100, pady=7)
            self.amounts[index].pack(side='bottom', anchor='w', expand=1, fill='x')
        # Question-----------------------------------------------------------
        self.mainFrame = Frame(self.windowRoot, bg='black')
        self.mainFrame.pack(side='left', anchor='w', expand=1, fill='x')
        # image
        self.image = Image.open('./img/logo.png')
        self.image = ImageTk.PhotoImage(self.image.resize((300, 280), Image.ANTIALIAS))
        self.logo = Label(self.mainFrame, image=self.image, compound='center', bg='black')
        self.logo.pack()
        # info frame
        self.infoFrame = Frame(self.mainFrame, bg='black')
        self.infoFrame.pack()
        # player name
        self.playerFrame = Frame(self.infoFrame, bg='black')
        self.playerFrame.pack(pady=10)
        self.playerLabel = Label(self.playerFrame, text='Player: ', bg='black', fg='white')
        self.playerLabel.grid(row=0, column=0)
        self.playerName = Label(self.playerFrame, textvariable=self.gameController.playerName, bg='black', fg='white')
        self.playerName.grid(row=0, column=1)
        # lives
        self.livesFrame = Frame(self.infoFrame, bg='black')
        self.livesFrame.pack(pady=10)
        self.livesLabel = Label(self.livesFrame, text='Lives:', bg='black', fg='white')
        self.livesLabel.grid(row=0, column=0)
        self.livesNum = Label(self.livesFrame, textvariable=self.gameController.lives, bg='black', fg='white')
        self.livesNum.grid(row=0, column=1)
        # timer
        # self.timerFrame = Frame(self.infoFrame)
        # self.timerFrame.pack(pady=10)
        # self.timerLabel = Label(self.timerFrame, text='Timer:')
        # self.timerLabel.grid(row=0, column=0)
        self.timerNum = Timer(self.infoFrame, imgPath=resourcePath(
            './img/clockNormal.png'), textvariable=self.gameController.timer)
        self.timerNum.pack(pady=10)

        # question frame
        self.questionFrame = Frame(self.mainFrame, bg='black')
        self.questionFrame.pack(side='bottom', anchor='s', expand=1, fill='both')
        # question text
        self.questionText = Label(self.questionFrame, textvariable=self.gameController.questionText,
                                  font=('sans-serif', 12, 'bold'), wraplength=600, bg='black', fg='white')
        self.questionText.pack()
        # answers
        self.answersFrame = Frame(self.questionFrame, bg='black')
        self.answersFrame.pack()
        self.answersFrame.rowconfigure((0, 1), minsize=ANSWERHEIGHT + 10)
        self.answersFrame.columnconfigure((0, 1), minsize=ANSWERWIDTH + 10)
        self.answers = [AAnswerButton] * 4
        for index, answer in enumerate(self.gameController.questionAnswers):
            self.answers[index] = AAnswerButton(self.answersFrame, textvariable=answer,
                                                callback=self.gameController.checkAnswer)
            self.answers[index].grid(row=index // 2, column=index % 2, pady=10, padx=10)
