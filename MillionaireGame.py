from tkinter import *
from typedef import *
from constants import *
from dbAPI import *
from Menu import *
from Game import *
from time import time
import colorama


# -----------------


class Player:
    def __init__(
        self,
        username: str = 'Player',
        money: int = 0,
        totalTime: float = 0,
        meanTime: float = 0,
        score: float = 0
    ) -> None:

        self.username = username
        self.money = money
        self.totalTime = totalTime
        self.meanTime = meanTime
        self.score = score



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
        if self.question['correct'] == self.selectedAnswer:
            return True
        return False


class MainWindow:
    def __init__(self) -> None:
        self.win = Tk()
        self.win.title('ΠΟΙΟΣ ΘΕΛΕΙ ΝΑ ΓΙΝΕΙ ΕΚΑΤΟΜΜΥΡΙΟΥΧΟΣ')
        self.win.iconbitmap('./img/icon.ico')
        self.win.geometry('800x600')
        self.win.config(background='black')
        self.win.minsize(width=1150, height=720)
        self.fullscreen = True
        self.win.attributes('-fullscreen', self.fullscreen)
        self.win.bind('<F11>', self.toggleFullscreen)
        self.win.bind('<Escape>', self.endFullscreen)

    def getRootWidget(self):
        return self.win

    def toggleFullscreen(self, event=None) -> None:
        self.fullscreen = not self.fullscreen   # toggling the boolean
        self.win.attributes('-fullscreen', self.fullscreen)
        return 'break'

    def endFullscreen(self, event=None) -> None:
        self.fullscreen = False
        self.win.attributes('-fullscreen', self.fullscreen)
        return 'break'

    def setLevel(self, level: str) -> None:
        # First, delete all widgets inside the main window
        for child in self.win.winfo_children():
            child.destroy()

        if level == MAINMENU:
            self.mainMenu = MainMenuLevel(self.win, lambda: self.setLevel(GAME))
            return
        if level == GAME:
            print('> IN GAME MODE')   #TODO DELETE
            self.clearWidgets()
            self.gameLevel = GameLevel(self.win)
            return
        if level == HALLOFFAME:
            return
        print('Error, wrong level string!')

    def clearWidgets(self):
        for child in self.win.winfo_children():
            child.destroy()

colorama.init()

# Main window
mainWindow = MainWindow()

mainWindow.setLevel(MAINMENU)

mainWindow.win.mainloop()
