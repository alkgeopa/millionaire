from __future__ import annotations
from typing import TYPE_CHECKING, Type

from tkinter import Misc, Frame, Label, IntVar, StringVar
from numpy.random import choice, shuffle
from time import time

from widgets import *
from dbAPI import getQuestions, getRandomQuestion

if TYPE_CHECKING:
    from main import MainWindow
    from typedef import Document


class GameLevel:
    def __init__(self, root: MainWindow) -> None:
        self.windowRoot = root

        # state variables
        self.maxLives = 3
        self.lives = self.maxLives
        self.livesVar = IntVar(value=self.maxLives)
        self.stage = 0
        self.level = 0
        self.skipJump = 0
        self.amountWon = StringVar(value='0 €')

        # time variables
        self.timeStart = time()
        self.timerVar = IntVar(value=5 + 1)
        self.questionTime = None
        self.timerAfter: str = None

        # question details
        self.questionPool = getQuestions()
        self.currentQuestion: Document = self.getCurrentQuestion()
        self.answerTexts: list[str] = []
        # question StrVars
        self.questionText = StringVar()
        self.answerTextVars: list[StringVar] = []
        for i in range(4):
            self.answerTextVars.append(StringVar())

        #-----------------------------------------------------------
        self.gameLevel = Frame(self.windowRoot, bg='black')
        self.gameLevel.place(relx=0.5, rely=0.5, anchor='center')
        # info widgets
        self.infoFrame = Frame(self.windowRoot)
        self.infoFrame.pack()
        # lives
        self.livesFrame = Frame(self.infoFrame)
        self.livesFrame.pack(pady=10)
        self.livesLabel = Label(self.livesFrame, text='Lives:')
        self.livesLabel.grid(row=0, column=0)
        self.livesNum = Label(self.livesFrame, textvariable=self.livesVar)
        self.livesNum.grid(row=0, column=1)
        # timer
        self.timerFrame = Frame(self.infoFrame)
        self.timerFrame.pack(pady=10)
        self.timerLabel = Label(self.timerFrame, text='Timer:')
        self.timerLabel.grid(row=0, column=0)
        self.timerNum = Label(self.timerFrame, textvariable=self.timerVar)
        self.timerNum.grid(row=0, column=1)
        self.updateTimer()

        # question widgets
        self.questionText = Label(self.gameLevel, textvariable=self.questionText,
                                  font=('sans-serif', 12, 'bold'), wraplength=600)
        self.questionText.pack()
        # answers
        self.answersFrame = Frame(self.gameLevel, bg='black')
        self.answersFrame.pack()
        self.answersFrame.rowconfigure((0, 1), minsize=ANSWERHEIGHT + 10)
        self.answersFrame.columnconfigure((0, 1), minsize=ANSWERWIDTH + 10)
        self.answers = [AAnswerButton] * 4
        for index, answer in enumerate(self.answerTexts):
            answer.set(f'{AAnswerButton.textPrefix[index]}{answer.get()}')
            self.answers[index] = AAnswerButton(self.answersFrame, textvariable=answer,
                                                callback=self.checkAnswer,)
            self.answers[index].grid(row=index // 2, column=index % 2, pady=10, padx=10)


    def changeLevel(self, newLevel: type[MenuLevel] | type[GameLevel] | type[TopTenLevel]):
        self.currentLevel = newLevel(self.windowRoot, self)
        self.initCurrentLevel()

    def initCurrentLevel(self):
        if type(self.currentLevel).__name__ == 'MenuLevel':
            return
        if type(self.currentLevel).__name__ == 'GameLevel':

            # state variables
            self.maxLives = 3
            self.lives = self.maxLives
            self.livesVar = IntVar(value=self.maxLives)
            self.stage = 0
            self.level = 0
            self.skipJump = 0
            self.amountWon = StringVar(value='0 €')

            # time variables
            self.timeStart = time()
            self.timerVar = IntVar(value=5 + 1)
            self.timerAfter = None
            self.questionTime = None

            # question details
            self.questionPool = getQuestions()
            self.currentQuestion: Document = self.getCurrentQuestion()
            print(self.currentQuestion)
            self.answerTexts: list[str] = []
            # question StrVars
            self.questionText = StringVar()
            self.answerTextVars: list[StringVar] = []
            for i in range(4):
                self.answerTextVars.append(StringVar())

            # self.initQuestionVars()
            self.setUpQuestionVars()
            return
        if type(self.currentLevel).__name__ == 'TopTenLevel':
            return

    def initQuestionVars(self):
        self.questionText.set(self.currentQuestion['text'])
        for index, ansWidget in enumerate(self.currentLevel.answers):
            ansWidget.config(textvariable=self.answerTextVars[index])

    def shuffleAnswers(self):
        self.answerTexts.append(self.currentQuestion['correct'])
        for answer in self.currentQuestion['wrong'].values():
            self.answerTexts.append(answer)
        shuffle(self.answerTexts)

    def setUpQuestionVars(self):
        self.questionText.set(self.currentQuestion['text'])
        self.shuffleAnswers()
        for index, answer in enumerate(self.answerTextVars):
            answer.set(self.answerTexts[index])
            self.currentLevel.answers[index].text = self.answerTexts[index]

    def resetWidgets(self):
        for index, answerWidget in enumerate(self.currentLevel.answers):
            answerWidget.changeNormalColor()
            answerWidget.grid(row=index // 2, column=index % 2, pady=10, padx=10)

    def getCurrentQuestion(self):
        if self.stage == 0:
            return self.questionPool['easy'].pop()
        if self.stage == 1:
            return self.questionPool['medium'].pop()
        if self.stage == 2:
            return self.questionPool['hard'].pop()

    def checkConditionsForNextQuestion(self):
        if self.level < 14:
            self.goToNextQuestion()
        else:
            ...  # you won

    def goToNextQuestion(self):
        self.level += 1
        self.currentQuestion = self.getCurrentQuestion()
        self.setUpQuestionVars()
        self.resetWidgets()

    def updateLives(self):
        self.livesVar.set(self.livesVar.get() - 1)

    def checkAnswer(self, event: Event):
        widget: AAnswerButton = event.widget
        widget.changeSelectionColor()
        if widget.text == self.currentQuestion['correct']:
            print(f'Selected the CORRECT answer.')
            self.windowRoot.after(4000, widget.changeCorrectColor)
            self.windowRoot.after(8000, self.checkConditionsForNextQuestion)
        else:
            print(f'Seleted the WRONG answer.')
            self.windowRoot.after(4000, widget.changeWrongColor)
            for ansWidget in self.currentLevel.answers:
                if ansWidget.text == self.currentQuestion['correct']:
                    self.windowRoot.after(4000, ansWidget.changeCorrectColor)

    def updateTimer(self):
        self.timerAfter = self.windowRoot.after(1000, self.updateTimer)

    def destroy(self):
        self.gameLevel.destroy()



class MenuLevel:
    def __init__(self, root: MainWindow) -> None:
        self.windowRoot = root

        # ---------------------------------------------------
        self.menuLevel = Frame(self.windowRoot, bg='black')
        self.menuLevel.place(relx=0.5, rely=0.5, anchor='center')

        self.title = Label(self.menuLevel, text='ΠΟΙΟΣ ΘΕΛΕΙ ΝΑ ΓΙΝΕΙ ΕΚΑΤΟΜΜΥΡΙΟΥΧΟΣ', font=(
            'san-serif', 40, 'bold'), bg='black', fg='white', wraplength=600)
        self.title.pack()

        self.btnStart = AMenuButton(
            master=self.menuLevel, text='Start', font=('san-serif', 20, 'bold'),
            width=10, height=1, command=self.startHandler)
        self.btnStart.pack(pady=20)
        self.btnTopTen = AMenuButton(
            master=self.menuLevel, text='Top 10', font=('san-serif', 20, 'bold'),
            width=10, height=1, command=self.topTenHandler)
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



class TopTenLevel:
    def __init__(self, root: MainWindow) -> None:
        self.windowroot = root
