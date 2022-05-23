from tkinter import Tk

from pygame import mixer

from controller import MenuLevel, GameLevel, TopTenLevel





class MainWindow(Tk):
    def __init__(self) -> None:
        super().__init__()
        self.currentView = None
        self.title("ΠΟΙΟΣ ΘΕΛΕΙ ΝΑ ΓΙΝΕΙ ΕΚΑΤΟΜΜΥΡΙΟΥΧΟΣ")
        self.geometry("1200x800+0+0")
        self["bg"] = "black"

        self.currentLevel: MenuLevel | GameLevel = MenuLevel(self)

    def changeLevel(self, newLevel: str):
        if self.currentLevel:
            self.currentLevel.destroy()
        if newLevel == 'GameLevel':
            self.currentLevel = GameLevel(self)
        if newLevel == 'TopTenLevel':
            self.currentLevel = TopTenLevel(self)



if __name__ == '__main__':
    mixer.init()

    mainWindow = MainWindow()

    mainWindow.mainloop()
