from tkinter import Tk, Frame
from constants import *
from pygame import mixer
from ViewMainMenu import *
from ViewUsernameInput import *
from GameController import *


class ApplicationController:
    def __init__(self, root: Tk, view: str = None) -> None:
        self.appRoot = root
        self.currentView: str = None
        self.currentViewFrame: Frame = None
        self.gameController: GameController = None
        self.setView(MAINMENU)

        mixer.init()

    def setView(self, view: str) -> Frame:
        if view in VIEWS:
            self.currentView = view
        else:
            raise Exception(f'"{view}" is not in the provided constants.VIEWS list')

        if view == MAINMENU:
            self.currentViewFrame = self.viewMainMenu()
            return

    def clearView(self) -> None:
        self.currentViewFrame.destroy()

    def viewMainMenu(self) -> MainMenu:
        return MainMenu(master=self.appRoot)

    def viewUserInput(self) -> MainMenu:
        return UsernameInput(master=self.appRoot)

    def viewGame(self) -> MainMenu:
        return MainMenu(master=self.appRoot)

    def viewVictory(self) -> MainMenu:
        return MainMenu(master=self.appRoot)

    def viewDefeat(self) -> MainMenu:
        return MainMenu(master=self.appRoot)

    def viewHallOfFame(self) -> MainMenu:
        return MainMenu(master=self.appRoot)

    def initGameController(self) -> GameController:
        ...
