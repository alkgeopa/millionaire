from tkinter import Frame, Misc, Tk, Widget
from pygame import mixer
from colorama import Fore, Back, Style
from numpy.random import choice, shuffle
from typedef import Document, Callable
from constants import lifelines
from dbAPI import *


class GameController:
    globalWindow: Tk
    replaceQuestion: Callable
    goToNextQuestion: Callable
    currentStage: int
    currentQuestion: int
    question: Document
    answerWidgets: list
    availableLifelines: dict
    answerSelected: str
    allQuestions: dict
    currentPlayer: str

    @classmethod
    def printDebug(self):
        print("-" * 60)
        print(f'{"currentStage:":20}{GameController.currentStage}')
        print(f'{"currentQuestion:":20}{GameController.currentQuestion}')
        print(f'{"questionText:":20}{GameController.question["text"]}')
        print(f'{"answerCorrect:":20}{GameController.question["correct"]}')
        print("." * 20)

    @classmethod
    def initGameController(self, window) -> None:
        GameController.globalWindow = window
        GameController.currentStage = 0
        GameController.currentQuestion = 0
        GameController.availableLifelines = {}
        for lifeline in lifelines:
            print(lifeline)
            GameController.availableLifelines[lifeline] = None

        print(GameController.availableLifelines)
        GameController.answerSelected = None
        GameController.allQuestions = getQuestions()

    @classmethod
    def drawSidePanel(self, master: Misc | None = ..., **kw):
        ...

    @classmethod
    def drawQuestion(self, master: Misc | None = ..., **kw):
        ...

    @classmethod
    def setStage(self) -> None:
        if GameController.currentQuestion < 5:
            GameController.currentStage = 0
            return
        if GameController.currentQuestion < 10:
            GameController.currentStage = 1
            return
        GameController.currentStage = 2

    @classmethod
    def getQuestion(self) -> Document:
        print(
            f"~In GameController.getQuestion(). currentStage={GameController.currentStage}"
        )
        if GameController.currentStage == 0:
            GameController.question = GameController.allQuestions["easy"].pop()
        if GameController.currentStage == 1:
            GameController.question = GameController.allQuestions["medium"].pop()
        if GameController.currentStage == 2:
            GameController.question = GameController.allQuestions["hard"].pop()

        print(f'>Getting question: {GameController.question["text"]}')
        return GameController.question

    @classmethod
    def lightCorrectAnswer(self):
        print(f"DEBUG: in lightCorrectAnswer()")
        for widget in GameController.answerWidgets:
            if widget.getAnswerText() == GameController.question["correct"]:
                widget.changeCorrectColor(playSound=False)

    @classmethod
    def registerAnswer(answer: str) -> None:
        GameController.answerSelected = answer

    @classmethod
    def checkAnswer(self) -> bool:
        if (
            GameController.answerSelected.strip()
            == GameController.question["correct"].strip()
        ):
            print(f"{GameController.answerSelected} >is CORRECT")
            return True
        print(f" `{GameController.answerSelected}` is WRONG")
        return False

    @classmethod
    def lifelineHandler(self, ident: str):
        if ident == "50-50":
            print(f"lifeline selected: {ident}")

            wrong = list(GameController.question["wrong"].values())
            shuffle(wrong)
            for answerWidget in GameController.answerWidgets:
                if answerWidget.getAnswerText().strip() in wrong[:-1]:
                    answerWidget.destroy()

            sfx = mixer.Sound("./sound/50-50.mp3")
            sfx.play()

            GameController.availableLifelines["50-50"].destroy()
            return
        if ident == "computer":
            print(f"lifeline selected: {ident}")
            weights: list[float] = []
            if GameController.currentQuestion < 5:
                for answerWidget in GameController.answerWidgets:
                    if (
                        answerWidget.getAnswerText().strip()
                        == GameController.question["correct"].strip()
                    ):
                        weights.append(0.91)
                    else:
                        weights.append(0.03)
            elif 5 <= GameController.currentQuestion < 10:
                for answerWidget in GameController.answerWidgets:
                    if (
                        answerWidget.getAnswerText().strip()
                        == GameController.question["correct"].strip()
                    ):
                        weights.append(0.76)
                    else:
                        weights.append(0.08)
            else:
                for answerWidget in GameController.answerWidgets:
                    if (
                        answerWidget.getAnswerText().strip()
                        == GameController.question["correct"].strip()
                    ):
                        weights.append(0.52)
                    else:
                        weights.append(0.16)

            suggestion = choice(GameController.answerWidgets, p=weights)
            print(f"Suggeston: {suggestion.getAnswerText().strip()}")
            suggestion.changeSuggestionColor()

            GameController.availableLifelines["computer"].destroy()
            return
        if ident == "skip":
            print(f"lifeline selected: {ident}")
            GameController.replaceQuestion()

            GameController.availableLifelines["skip"].destroy()
            return

    @classmethod
    def nextQuestion(self) -> None:
        GameController.currentQuestion += 1
        GameController.setStage()
        print(
            f"> Going to question {GameController.currentQuestion + 1}, stage: {GameController.currentStage}"
        )
        GameController.goToNextQuestion()
        GameController.answerSelected = ""

    @classmethod
    def win(self):
        print(f"{Back.GREEN}{Fore.BLACK}⭐YOU HAVE WON!⭐{Style.RESET_ALL}")  #!

    @classmethod
    def defeat(self):
        print(f"{Back.RED}{Fore.BLACK}😓YOU HAVE LOST!😓{Style.RESET_ALL}")  #!
