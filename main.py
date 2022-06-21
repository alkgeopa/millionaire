from tkinter import Tk

from controller import Controller, GameController
from gameLevel import GameLevel
from menuLevel import MenuLevel
from topTenView import TopTenView


class MainWindow(Tk):
    def __init__(self) -> None:
        super().__init__()
        self.currentView = None
        self.title("ΠΟΙΟΣ ΘΕΛΕΙ ΝΑ ΓΙΝΕΙ ΕΚΑΤΟΜΜΥΡΙΟΥΧΟΣ")
        self.geometry("1200x800+0+0")
        self["bg"] = "black"
        self.state = True
        self.attributes("-fullscreen", self.state)
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)
        self.currentLevel: MenuLevel | GameLevel = MenuLevel(self)
        self.controller: type[Controller] | type[GameController] = Controller
        self.controller.root = self

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.attributes("-fullscreen", False)
        return "break"

    def changeLevel(self, newLevel: str):
        if self.currentLevel:
            self.currentLevel.destroy()
        if newLevel == 'GameLevel':
            self.controller = GameController
            self.controller.init()
        if newLevel == 'TopTenLevel':
            self.currentLevel = TopTenView(self)
        if newLevel == 'MainMenu':
            self.currentLevel = MenuLevel(self)


if __name__ == '__main__':
    mainWindow = MainWindow()
    mainWindow.mainloop()
