from tkinter import *
from Menu import *
from time import time
from typedef import *
from constants import *
from dbAPI import *


# -----------------


class Player:
    def __init__(
            self,
            username: str = 'Player',
            money: int = 0,
            totalTime: float = 0,
            meanTime: float = 0,
            score: float = 0) -> None:

        self.username = username
        self.money = money
        self.totalTime = totalTime
        self.meanTime = meanTime
        self.score = score


class Game:
    state = {}

    @staticmethod
    def resetGameState():
        Game.state = {
            'currentView': None,
            'started': NO,
            'stage': None,
            'victory': None,
        }


class HallOfFame:
    pass


class Question:
    def __init__(self, info: Document) -> None:
        self.question = info

        self.timeStart = time()
        self.timeEnd: float = None
        self.time: float = None

        self.selectedAnswer = ''

    def calculateQuestionTime(self) -> None:
        self.time = self.timeEnd - self.timeStart if self.timeEnd else None

    def getQuestionTime(self) -> float:
        return self.time

    def setSelectedAnswer(self, answer: str) -> None:
        self.selectedAnswer = answer

    def checkSelectedAnswer(self) -> bool:
        if self.question['wrong'] == self.selectedAnswer:
            return True
        return False


class Lifeline:
    pass


class Money:
    pass


class MainWindow:
    def __init__(self) -> None:
        self.win = Tk()
        self.win.title('ΠΟΙΟΣ ΘΕΛΕΙ ΝΑ ΓΙΝΕΙ ΕΚΑΤΟΜΜΥΡΙΟΥΧΟΣ')
        self.win.iconbitmap('./img/icon.ico')
        self.win.geometry('800x600')
        self.win.config(background='black')
        self.win.minsize(width=800, height=600)
        self.fullscreen = True
        self.win.attributes('-fullscreen', self.fullscreen)
        self.win.bind('<F11>', self.toggleFullscreen)
        self.win.bind('<Escape>', self.endFullscreen)

    def toggleFullscreen(self, event=None):
        self.fullscreen = not self.fullscreen   # toggling the boolean
        self.win.attributes('-fullscreen', self.fullscreen)
        return 'break'

    def endFullscreen(self, event=None):
        self.fullscreen = False
        self.win.attributes('-fullscreen', self.fullscreen)
        return 'break'

    def setLevel(self, level: str):
        # First, delete all widgets inside the main window
        for child in self.win.winfo_children():
            child.destroy()

        if level == MAINMENU:
            self.mainMenu = MainMenuLevel(self.win, lambda: self.setLevel(GAME))
            return
        if level == GAME:
            print('IN GAME MODE')   #TODO DELETE
            self.win.destroy()  #TODO DELETE
            return
        if level == HALLOFFAME:
            return
        print('Error, wrong level string!')


# Main window
mainWindow = MainWindow()

mainWindow.setLevel(MAINMENU)

mainWindow.win.mainloop()
