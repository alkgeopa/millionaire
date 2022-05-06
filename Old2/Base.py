from tkinter import *
from typedef import *
from constants import *
from ApplicationController import *
import colorama


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
        self.appController = ApplicationController(self, MAINMENU)

    def getRootWidget(self):
        return self

    def toggleFullscreen(self, event: Event = None) -> None:
        self.fullscreen = not self.fullscreen   # toggling the boolean
        self.attributes('-fullscreen', self.fullscreen)
        return 'break'

    def endFullscreen(self, event: Event = None) -> None:
        self.fullscreen = False
        self.attributes('-fullscreen', self.fullscreen)
        return 'break'

    def clearWidgets(self):
        for child in self.winfo_children():
            child.destroy()


colorama.init()

# Main window
mainWindow = MainWindow()

mainWindow.mainloop()
