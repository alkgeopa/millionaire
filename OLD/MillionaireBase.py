from tkinter import *
from typedef import *
from constants import *
from dbAPI import *
from Menu import *
from Game import *
from time import time
import colorama


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


class MainWindow(Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title('ΠΟΙΟΣ ΘΕΛΕΙ ΝΑ ΓΙΝΕΙ ΕΚΑΤΟΜΜΥΡΙΟΥΧΟΣ')
        self.iconbitmap('./img/icon.ico')
        self.geometry('800x600')
        self.config(background='black')
        self.minsize(width=1150, height=720)
        self.fullscreen = True
        self.attributes('-fullscreen', self.fullscreen)
        self.bind('<F11>', self.toggleFullscreen)
        self.bind('<Escape>', self.endFullscreen)

    def getRootWidget(self):
        return self

    def toggleFullscreen(self, event: Event=None) -> None:
        self.fullscreen = not self.fullscreen   # toggling the boolean
        self.attributes('-fullscreen', self.fullscreen)
        return 'break'

    def endFullscreen(self, event: Event=None) -> None:
        self.fullscreen = False
        self.attributes('-fullscreen', self.fullscreen)
        return 'break'

    def setLevel(self, level: str) -> None:
        # First, delete all widgets inside the main window
        for child in self.winfo_children():
            child.destroy()

        if level == MAINMENU:
            self.mainMenu = MainMenuLevel(self, lambda: self.setLevel(GAME))
            return
        if level == GAME:
            print('> IN GAME MODE')   #TODO DELETE
            self.clearWidgets()
            self.gameLevel = GameLevel(self)
            return
        if level == HALLOFFAME:
            return
        print('Error, wrong level string!')

    def clearWidgets(self):
        for child in self.winfo_children():
            child.destroy()

colorama.init()

# Main window
mainWindow = MainWindow()

mainWindow.setLevel(MAINMENU)

mainWindow.mainloop()
