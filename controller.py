import re
from tkinter import *
from pygame import mixer
from typing import TYPE_CHECKING

from time import time

from numpy.random import shuffle, choice
from names import get_first_name

from constants import *
from dbAPI import getRandomQuestion, getTopTenPlayers, getQuestions
from filePath import resourcePath
from gameView import GameView
from menuView import MainMenu
from playerNameInputView import PlayerNameInputView
from questionFrame import QuestionFrame
from sidePanelFrame import SidePanelFrame
from topTenView import TopTenView
from resultViews import VictoryView, DefeatView


if TYPE_CHECKING:
    from main import MainWindow


class Controller:
    appRoot: 'MainWindow' = None

    def __init__(self) -> None:
        ...


class ApplicationController(Controller):
    def __init__(self, appRoot: 'MainWindow') -> None:
        super(ApplicationController, self).__init__()
        Controller.appRoot = appRoot
        self.currentController = MainMenuController(self)

    def setController(self, controller):
        self.currentController: MainMenuController | PlayerNameController | GameController | TopTenController = controller()


class MainMenuController(Controller):
    def __init__(self, appController) -> None:
        super(MainMenuController, self).__init__()
        self.appController: ApplicationController = appController
        self.currentView: MainMenu | GameView = MainMenu(self.appRoot, self)
        mixer.music.load('./sound/main-theme.mp3')
        mixer.music.play(loops=-1)
        mixer.music.set_volume(0.3)

    def startHandler(self):
        self.currentView.destroy()
        mixer.music.fadeout(200)
        self.appController.setController(lambda: PlayerNameController(self.appController))

    def topTenHandler(self):
        self.currentView.destroy()
        self.appController.setController(lambda: TopTenController(self.appController))


class PlayerNameController(Controller):
    def __init__(self, appController) -> None:
        super(PlayerNameController, self).__init__()
        self.appController: ApplicationController = appController
        self.playerName = StringVar(value=get_first_name())
        self.currentView = PlayerNameInputView(self.appRoot, self)
        self.sfx = mixer.Sound(resourcePath('./sound/lets-play.mp3'))
        self.sfx.set_volume(0.1)
        self.sfx.play()

    def startHandler(self):
        print(f'{self.playerName.get() = }')
        self.sfx.fadeout(500)
        self.currentView.destroy()
        self.appController.setController(lambda: GameController(self.appController, self.playerName))


class GameController(Controller):
    def __init__(self, appController: ApplicationController, playerName: StringVar = None) -> None:
        super(GameController, self).__init__()
        self.maxLives = 3
        self.lives = self.maxLives
        self.stage = 0
        self.level = 0
        self.skipJump = 0

        self.amountWon = StringVar(value='0 €')

        self.questionPool = getQuestions()

        self.appController = appController
        self.gameView = GameView(self.appRoot)

        self.playerName = playerName
        self.questionTimes: list[float] = []
        self.score: float = None

        self.gameSounds = {
            'suggestion-answer': mixer.Sound(resourcePath('./sound/suggestion-answer.mp3')),
            'correct-answer': mixer.Sound(resourcePath('./sound/correct-answer.mp3')),
            'wrong-answer': mixer.Sound(resourcePath('./sound/wrong-answer.mp3')),
            'final-answer': mixer.Sound(resourcePath('./sound/final-answer.mp3')),
            'question': mixer.Sound(resourcePath('./sound/question.mp3')),
            '50-50': mixer.Sound(resourcePath('./sound/50-50.mp3')),
            'outOfTime': mixer.Sound(resourcePath('./sound/outOfTime.mp3')),
        }

        self.questionController = QuestionController(self.gameView, self)
        self.questionController.questionInit()

        

        self.lifelinesController = LifelineController(self.gameView, self)

        self.sidePanel = SidePanelFrame(self.gameView, self.lifelinesController)

        self.gameSounds['question'].set_volume(0.2)
        self.gameSounds['question'].play(loops=-1, fade_ms=1000)

    def lifelineHandler(self, event: Event):
        if event.widget.text == "50-50":
            event.widget.destroy()
            self.questionController.fiftyFifty()
            self.gameSounds['50-50'].play()
            return
        if event.widget.text == "computer":
            event.widget.destroy()

            weights: list[float] = []
            if self.level < 5:
                for answerButton in self.questionController.questionFrame.answers:
                    if answerButton.text.strip() == self.questionController.correctAnswer:
                        weights.append(0.82)
                    else:
                        weights.append(0.06)
            elif 5 <= self.level < 10:
                for answerButton in self.questionController.questionFrame.answers:
                    if answerButton.text.strip() == self.questionController.correctAnswer:
                        weights.append(0.67)
                    else:
                        weights.append(0.11)
            else:
                for answerButton in self.questionController.questionFrame.answers:
                    if answerButton.text.strip() == self.questionController.correctAnswer:
                        weights.append(0.49)
                    else:
                        weights.append(0.17)
            suggestion = choice(self.questionController.questionFrame.answers, p=weights)
            suggestion.changeSuggestionColor()
            suggestion.suggestionAnswerSFX.play(loops=0)
            suggestion.suggestionAnswerSFX.set_volume(0.2)
            print(f"Suggeston:\t{suggestion.text.strip()}")

            return
        if event.widget.text == "skip":
            event.widget.destroy()
            self.skipJump = 1
            self.questionController.questionFrame.destroy()
            self.questionController = QuestionController(self.gameView, self)
            self.questionController.questionInit()
            return

    def updateLives(self):
        self.lives -= 1
        self.questionController.questionFrame.lives.pop().disable()

    def checkSafetyNet(self):
        if self.stage == 1:
            self.amountWon.set(f'{AMOUNTS[4]} €')
            self.triggerEndView(view='victory')
        elif self.stage == 2:
            self.amountWon.set(f'{AMOUNTS[9]} €')
            self.triggerEndView(view='victory')
        else:
            self.triggerEndView(view='defeat')

    def setStage(self) -> None:
        if self.level < 5:
            self.stage = 0
            return
        if self.level < 10:
            self.stage = 1
            return
        self.stage = 2

    def getNextQuestion(self):
        if self.stage == 0:
            return self.questionPool['easy'].pop()
        if self.stage == 1:
            return self.questionPool['medium'].pop()
        if self.stage == 2:
            return self.questionPool['hard'].pop()

    def nextQuestion(self, result: str):
        if self.lives > 0 and self.level < 14:
            if result == 'correct':
                self.level += 1
                self.setStage()
                self.replaceQuestion()

                self.sidePanel.destroy()
                self.sidePanel = SidePanelFrame(self.gameView, self.lifelinesController)
            else:
                self.replaceQuestion()
        else:
            self.checkSafetyNet()

    def replaceQuestion(self):
        self.questionController.questionFrame.destroy()
        del self.questionController
        self.questionController = QuestionController(self.gameView, self)
        self.questionController.questionInit()
        self.gameSounds['question'].set_volume(0.2)
        self.gameSounds['question'].play(loops=-1, fade_ms=1000)

    def triggerEndView(self, view: str):
        if view == 'victory':
            self.questionController.questionFrame.destroy()
            self.sidePanel.destroy()
            del self.questionController
            self.endView = VictoryView(master=self.gameView, controller=self)
            self.calculatePlayerStatistics()
        if view == 'defeat':
            self.questionController.questionFrame.destroy()
            self.sidePanel.destroy()
            del self.questionController
            self.endView = DefeatView(master=self.gameView, controller=self)

    def calculatePlayerStatistics(self) -> list:
        amountWon = re.sub('.|€| ', AMOUNTS[self.level])
        print(f'{amountWon = }')
        totalTime = sum(self.questionTimes)

    def mainMenuView(self):
        self.gameView.destroy()
        self.appController.setController(lambda: MainMenuController(self.appController))


class QuestionController(Controller):
    def __init__(self, root: GameView, gameController: GameController) -> None:
        super(QuestionController, self).__init__()

        self.gameController = gameController
        self.gameRoot = root
        self.questionFrame: QuestionFrame = None
        questionInfo = self.gameController.getNextQuestion()

        self.questionText = questionInfo["text"]
        self.correctAnswer = questionInfo["correct"]
        self.wrongAnswers = questionInfo["wrong"]
        self.shuffledAnswers = []
        self.shuffledAnswers.append(self.correctAnswer)
        for answer in self.wrongAnswers.values():
            self.shuffledAnswers.append(answer)
        shuffle(self.shuffledAnswers)

        print('-' * 10)
        print(f'stage:\t\t{self.gameController.stage}')
        print(f'level:\t\t{self.gameController.level}')
        print(f'lives:\t\t{self.gameController.lives}')
        print(f'questionText:\t{self.questionText}')
        print(f'correctAnswer:\t{self.correctAnswer}')
        print(f'shuffledAnswers:{self.shuffledAnswers}')

        self.selectedAnswer = ""

        self.timeStart = time()
        self.timerVar = IntVar(value=60 + 1)
        self.timerAfter: float = None
        self.questionTime: float = None

    def __del__(self):
        print(f'Deleted {self}')

    def initTimer(self):
        self.gameRoot.after_cancel(self.timerAfter)
        self.timeStart = time()
        self.questionTime = 0.0
        self.timerVar = IntVar(value=60 + 1)
        self.timerAfter = None
        self.questionTime = None

    def updateTimer(self):
        self.timerVar.set(self.timerVar.get() - 1)
        if self.timerVar.get() > 0:
            self.timerAfter = self.gameRoot.after(1000, self.updateTimer)

    def questionInit(self):
        self.questionFrame = QuestionFrame(self.gameRoot, self)

    def checkAnswer(self, event: Event):
        self.questionTime = time() - self.timeStart
        if not self.selectedAnswer:
            if self.timerAfter:
                self.gameRoot.after_cancel(self.timerAfter)
            self.questionTime = time() - self.timeStart
            self.selectedAnswer = event.widget.text.strip()

            self.gameController.gameSounds['question'].fadeout(200)
            event.widget.finalAnswerSFX.play()
            event.widget.finalAnswerSFX.set_volume(0.5)
            event.widget.setButtonImage('./img/answerSelection.png')
            event.widget.resizeButtonImage(300, 50)

            print(f'questionTime:\t{self.questionTime}')
            print(f"selectedAnswer:\t{self.selectedAnswer}")
            if self.selectedAnswer == self.correctAnswer:
                self.gameController.questionTimes.append(self.questionTime)
                print("Selected the CORRECT answer")
                event.widget.after(4000, lambda: self.correctColor(event.widget))
                event.widget.after(8000, self.gameController.nextQuestion, 'correct')
            else:
                print("Selected the WRONG answer")
                for button in self.questionFrame.answers:
                    if self.correctAnswer == button.text:
                        event.widget.after(4000, lambda: self.wrongColor(button, event.widget))
                        event.widget.after(4000, self.gameController.updateLives)
                        event.widget.after(8000, self.gameController.nextQuestion, 'wrong')

    @staticmethod
    def correctColor(button) -> None:
        button.changeCorrectColor()
        button.correctAnswerSFX.play(loops=0, fade_ms=100)
        button.correctAnswerSFX.set_volume(0.5)
        button.finalAnswerSFX.stop()
        button.after(3000, button.correctAnswerSFX.fadeout, 1500)

    @staticmethod
    def wrongColor(correctButton, wrongButton) -> None:
        correctButton.changeCorrectColor()
        wrongButton.changeWrongColor()
        wrongButton.wrongAnswerSFX.play(loops=0, fade_ms=100)
        wrongButton.wrongAnswerSFX.set_volume(0.5)
        wrongButton.finalAnswerSFX.stop()

    # generator
    def getNextAnswer(self) -> str:
        for answer in self.shuffledAnswers:
            yield answer

    def fiftyFifty(self) -> None:
        wrong = list(self.wrongAnswers.values())
        shuffle(wrong)
        for answerButton in self.questionFrame.answers:
            if answerButton.text.strip() in wrong[:-1]:
                answerButton.destroy()


class LifelineController(Controller):
    def __init__(self, gameView: GameView, gameController: GameController) -> None:
        super(LifelineController, self).__init__()
        self.gameController = gameController
        self.lifelinesInfo = {}
        for lifeline in LIFELINES:
            self.lifelinesInfo[lifeline] = None

    def lifelineHandler(self, event):
        if event.widget.text == "50-50":
            print(f"lifeline selected: {event.widget.text}")
            self.gameController.lifelineHandler(event)
            del self.lifelinesInfo['50-50']
            return
        if event.widget.text == "computer":
            print(f"lifeline selected: {event.widget.text}")
            self.gameController.lifelineHandler(event)
            del self.lifelinesInfo['computer']
            return
        if event.widget.text == "skip":
            print(f"lifeline selected: {event.widget.text}")
            self.gameController.lifelineHandler(event)
            del self.lifelinesInfo['skip']
            return


class TopTenController(Controller):
    def __init__(self, appController: ApplicationController) -> None:
        super(TopTenController, self).__init__()
        self.appController = appController
        self.playersInfo = getTopTenPlayers()
        self.currentView = TopTenView(self.appRoot, self, self.playersInfo)

    # generator
    def getNextPlayer(self) -> None:
        for player in self.playersInfo:
            yield player
