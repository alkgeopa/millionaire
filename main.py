from tkinter import Tk

from pygame import mixer

from controller import ApplicationController





class MainWindow(Tk):
    def __init__(self) -> None:
        super().__init__()
        self.currentView = None
        self.title("ΠΟΙΟΣ ΘΕΛΕΙ ΝΑ ΓΙΝΕΙ ΕΚΑΤΟΜΜΥΡΙΟΥΧΟΣ")
        self.geometry("1200x800+0+0")
        self["bg"] = "black"
        self.appController = ApplicationController(self)

    def setView(self, view = None):
        self.currentView = view
        self.currentView.pack()

    def __str__(self):
        return 'Main Window'


mixer.init()

mainWindow = MainWindow()

mainWindow.mainloop()
