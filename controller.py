from __future__ import annotations

from copy import deepcopy
from time import time
from tkinter import Frame, IntVar, StringVar
from typing import TYPE_CHECKING

from numpy.random import choice, shuffle

from constants import LIFELINES
from dbAPI import getQuestions
from gameLevel import GameLevel
from playerNameInputView import PlayerNameInputView
from widgets import *

if TYPE_CHECKING:
    from main import MainWindow
    from typedef import Question


class Controller:
    root: MainWindow


class GameController(Controller):
    checkSpeed: float
    playerName: StringVar
    stage: int
    level: int
    lives: IntVar
    lifelines: list[str]
    currentView: Frame
    questionPool: list[list]
    questionText: StringVar
    correctAnswer: str
    questionAnswers: list[StringVar]
    timer: IntVar
    timerAfter: str

    @classmethod
    def init(cls):
        cls.checkSpeed = .1
        cls.playerName = StringVar(master=cls.root)
        cls.stage = 0
        cls.level = 0
        cls.lives = IntVar(master=cls.root, value=3)
        cls.lifelines = deepcopy(LIFELINES)
        cls.currentView: PlayerNameInputView | GameLevel = PlayerNameInputView(cls.root, cls)
        cls.timerAfter = ''

    @classmethod
    def playerNameStartHandler(cls):
        cls.currentView.destroy()
        cls.initQuestions()
        if not cls.playerName.get():
            cls.playerName.set('New Player')
        cls.currentView = GameLevel(cls.root, cls)
        cls.replaceQuestion()

    @classmethod
    def initQuestions(cls):
        cls.questionPool = getQuestions()
        cls.questionText = StringVar()
        cls.questionAnswers = []
        for index in range(4):
            cls.questionAnswers.append(StringVar(name=f'answer_{index}'))
        cls.timer = IntVar(master=cls.root, value=6+1)

    @classmethod
    def printQuestionInfo(cls):
        print('-'*30)
        print(f'level: {cls.level}')
        print(f'stage: {cls.stage}')
        print(f'lives: {cls.lives.get()}')
        print(f'question: {cls.questionText.get()}')
        print('answers: | ', end='')
        [print(f'{answer.get()}', end=" | ") for answer in cls.questionAnswers]
        print()
        print(f'correct: {cls.correctAnswer}')

    @classmethod
    def levelUp(cls):
        cls.level += 1
        cls.stage = cls.level // 5

    @classmethod
    def updateTimer(cls):
        if cls.timer.get() < 1:
            cls.checkCondition('wrong')
            return
        cls.timer.set(cls.timer.get() - 1)
        if cls.timer.get() < 5:
            cls.currentView.timerNum.changeToCritical()
        elif cls.timer.get() < 15:
            cls.currentView.timerNum.changeToLow()
        cls.timerAfter = cls.root.after(1000, cls.updateTimer)

    @classmethod
    def getNextQuestion(cls) -> Question:
        return cls.questionPool[cls.stage].pop()

    @classmethod
    def replaceQuestion(cls):
        if cls.timerAfter:
            cls.root.after_cancel(cls.timerAfter)
        question = cls.getNextQuestion()
        cls.questionText.set(question['text'])
        cls.correctAnswer = question['correct']
        answers = [question['correct']]
        [answers.append(w) for w in question['wrong'].values()]
        shuffle(answers)
        for index, answer in enumerate(answers):
            cls.questionAnswers[index].set(answer)
        cls.timer.set(6+1)
        cls.currentView.timerNum.changeToNormal()
        cls.restoreQuestion()
        cls.highlightCurrentAmount()
        cls.printQuestionInfo()
        cls.updateTimer()

    @classmethod
    def restoreQuestion(cls):
        for answer in cls.currentView.answers:
            answer.changeNormalColor()
            answer.enable()

    @classmethod
    def checkCondition(cls, result: str):
        if result == 'correct':
            cls.levelUp()
            if cls.level < 15:
                cls.replaceQuestion()
            else:
                print('Εκατομμυριούχος!!!')
        else:
            cls.lives.set(cls.lives.get() - 1)
            if cls.lives.get() > 0:
                cls.replaceQuestion()
            elif cls.stage:
                print('Μαξιλαράκι...')
                if cls.stage == 1:
                    cls.currentView.amounts[cls.level].config(bg='#440')
                    cls.currentView.amounts[4].config(bg='#ffb437', fg='black')
                if cls.stage == 2:
                    cls.currentView.amounts[cls.level].config(bg='#af7400')
                    cls.currentView.amounts[9].config(bg='#ffb437', fg='black')
            else:
                print('Εχασες!')

    @classmethod
    def highlightCurrentAmount(cls):
        if cls.level < 15:
            cls.currentView.amounts[cls.level].config(bg='#ffb437', fg='black')
        if cls.level > 0:
            cls.currentView.amounts[cls.level-1].config(bg='black', fg='#ffb437')

    @classmethod
    def checkAnswer(cls, event: Event):
        cls.root.after_cancel(cls.timerAfter)
        button: AAnswerButton = event.widget
        button.changeSelectionColor()
        answerVar = cls.questionAnswers[int(str(button["textvariable"])[-1])]
        print(f'selected: {answerVar.get()}')
        [answer.disable() for answer in cls.currentView.answers if answer.enable]
        if answerVar.get() == cls.correctAnswer:
            print('Selected the CORRECT answer')
            cls.root.after(int(cls.checkSpeed * 4000), button.changeCorrectColor)
            cls.root.after(int(cls.checkSpeed * 6000), cls.checkCondition, 'correct')
        else:
            print('Selected the WRONG answer')
            cls.root.after(int(cls.checkSpeed * 4000), button.changeWrongColor)
            for index, answer in enumerate(cls.questionAnswers):
                if answer.get() == cls.correctAnswer:
                    cls.root.after(int(cls.checkSpeed * 4000), cls.currentView.answers[index].changeCorrectColor)
            cls.root.after(int(int(cls.checkSpeed * 6000)), cls.checkCondition, 'wrong')

    @classmethod
    def lifelineDispatch(cls, event: Event):
        button: ALifelineButton = event.widget
        print(f'lifeline selected: {button.text}')
        if button.text == '50-50':
            cls.fiftyFifty()
        elif button.text == 'computer':
            cls.suggestAnswer()
        else:
            cls.replaceQuestion()
        button.destroy()

    @classmethod
    def suggestAnswer(cls):
        count = -1
        for answer in cls.currentView.answers:
            if answer.enable:
                count += 1

        if cls.stage == 0:
            weights = cls.assingWeights(0.7, 0.3, count)
        if cls.stage == 1:
            weights = cls.assingWeights(0.5002, 0.4998, count)
        if cls.stage == 2:
            weights = cls.assingWeights(0.37, 0.63, count)

        selection: AAnswerButton = choice(cls.currentView.answers, p=weights)
        selection.changeSuggestionColor()

    @classmethod
    def assingWeights(cls, cWeight, wWeight, wCount) -> list[float]:
        weights: list[float] = []
        for index, answer in enumerate(cls.currentView.answers):
            if answer.enable and not cls.questionAnswers[index].get() == cls.correctAnswer:
                weights.append(wWeight/wCount)
            elif not answer.enable:
                weights.append(0)
            else:
                weights.append(cWeight)
        print(f'weights: {weights}')
        return weights

    @classmethod
    def fiftyFifty(cls):
        indexList: list[int] = []
        for index, answer in enumerate(cls.currentView.answers):
            if not cls.questionAnswers[index].get() == cls.correctAnswer:
                indexList.append(index)

        indexList = list(choice(indexList, size=2, replace=False))
        for index, answer in enumerate(cls.currentView.answers):
            if index in indexList:
                answer.disable()
                cls.questionAnswers[index].set('')
