from tkinter import *
from PIL import Image, ImageTk
from pygame import mixer

from constants import ANSWERHEIGHT, ANSWERWIDTH


class AButton(Button):
    def __init__(self, master: Misc | None = ..., imgPath: str = None, **kw) -> None:
        super().__init__(master, **kw)
        self.buttonImage = None
        self.text = self["text"]

        self.defaultBackground = "black"
        self.defaultForeground = "white"
        if self["background"] == self["bg"] == "":
            self["background"] = self.defaultBackground
        self["foreground"] = self.defaultForeground
        self["activebackground"] = self.defaultBackground
        self["activeforeground"] = self.defaultForeground
        self.imagePath = imgPath

    def setButtonImage(self, path: str):
        self.imagePath = path
        self.buttonImage = Image.open(self.imagePath)
        self.buttonImage = ImageTk.PhotoImage(self.buttonImage)
        self.config(image=self.buttonImage)

    def resizeButtonImage(self, width=0, height=0):
        self.buttonImage = Image.open(self.imagePath)
        if not width == height == 0:
            self.buttonImage = self.buttonImage.resize((width, height), Image.ANTIALIAS)
        self.buttonImage = ImageTk.PhotoImage(self.buttonImage)
        self.config(image=self.buttonImage)

    @classmethod
    def aButtonHandler(cls):
        if cls.__name__ == "AAnswerButton":
            print(cls.__name__)
            return
        if cls.__name__ == "AMenuButton":
            print(cls.__name__)
            return
        if cls.__name__ == "ALifelineButton":
            print(cls.__name__)
            return


class AMenuButton(AButton):
    def __init__(self, master: Misc | None = ..., **kw) -> None:
        super().__init__(master, **kw)
        self["bg"] = "purple"


class AAnswerButton(AButton):
    textPrefix = ["A. ", "B. ", "Γ. ", "Δ. "]

    def __init__(self, master: Misc | None = ..., callback=None, **kw) -> None:
        super().__init__(master, **kw)

        self.finalAnswerSFX = mixer.Sound("./sound/final-answer.mp3")
        self.correctAnswerSFX = mixer.Sound("./sound/correct-answer.mp3")
        self.wrongAnswerSFX = mixer.Sound("./sound/wrong-answer.mp3")
        self.suggestionAnswerSFX = mixer.Sound("./sound/suggestion-answer.mp3")

        self.text = self["text"][3:].strip()

        self.imagePath = "./img/answerFrame.png"
        self.resizeButtonImage(300, 50)
        self.defaultBackground = "black"
        self.defaultForeground = "white"
        self["background"] = self.defaultBackground
        self["foreground"] = self.defaultForeground
        self["activeforeground"] = self.defaultForeground
        self["activebackground"] = "#111"
        self["font"] = ("Segoe UI", 9, "bold")
        self["pady"] = 10
        self["padx"] = 10
        self["border"] = 0
        self["relief"] = "flat"
        self["compound"] = "center"

        self["disabledforeground"] = "black"

        self.callback = callback
        self.bind("<1>", self.clickHandler)

    def clickHandler(self, event):
        self.callback(event)

    def changeCorrectColor(self):
        self.setButtonImage("./img/answerCorrect.png")
        self.resizeButtonImage(300, 50)

    def changeWrongColor(self):
        self.setButtonImage("./img/answerWrong.png")
        self.resizeButtonImage(300, 50)

    def changeSuggestionColor(self):
        self.setButtonImage("./img/answerSuggestion.png")
        self.resizeButtonImage(300, 50)


class ALifelineButton(AButton):
    def __init__(self, master, imgPath: str = None, callback=None, **kw):
        super().__init__(master, imgPath=imgPath, **kw)
        self.text = self["text"].strip()
        self["text"] = ""

        self["bg"] = self.defaultBackground  # black
        self["border"] = 0
        self["relief"] = FLAT
        self["background"] = "black"
        self["width"] = ANSWERWIDTH
        self["height"] = ANSWERHEIGHT
        self["command"] = None

        self.callback = callback

        self.bind("<1>", self.clickHandler)

    def clickHandler(self, event: Event):
        self.callback(event)
