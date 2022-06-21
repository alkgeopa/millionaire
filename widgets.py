from tkinter import *

from PIL import Image, ImageTk

from constants import ANSWERHEIGHT, ANSWERWIDTH
from filePath import resourcePath


class AButton(Button):
    def __init__(self, master: Misc | None = ..., imgPath: str | None = ..., callback=None, **kw):
        super().__init__(master, **kw)
        self.callback = callback
        self.buttonImage = None
        self.imagePath = imgPath
        self.enabled = True
        self.text = self["text"].strip()

        self.defaultBackground = "black"
        self.defaultForeground = "white"
        if self["background"] == self["bg"] == "":
            self["background"] = self.defaultBackground
        self.config(fg=self.defaultForeground, activebackground=self.defaultBackground,
                    activeforeground=self.defaultForeground, highlightbackground=self.defaultBackground)

        self.bindClick = self.bind("<1>", self.clickHandler)

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

    def clickHandler(self, event: Event):
        if self.callback:
            self.callback(event)
        else:
            print(f'No callback for {__class__} button {self.text}.')

    def disable(self, hide: bool = False):
        self.enabled = False
        self.bindClick = self.bind('<1>', lambda _: 'break')

    def enable(self):
        self.enabled = True
        self.bindClick = self.bind("<1>", self.clickHandler)


class AMenuButton(AButton):
    def __init__(self, master: Misc | None = ..., **kw):
        super().__init__(master, **kw)
        self["bg"] = "purple"


class AAnswerButton(AButton):
    """Answer button variant"""
    textPrefix = ["A. ", "B. ", "Γ. ", "Δ. "]

    def __init__(self, master: Misc | None = ..., imgPath: str | None = ..., callback=None, **kw) -> None:
        super().__init__(master, imgPath=imgPath, callback=callback, **kw)

        # self.finalAnswerSFX = mixer.Sound(resourcePath("./sound/final-answer.mp3"))
        # self.correctAnswerSFX = mixer.Sound(resourcePath("./sound/correct-answer.mp3"))
        # self.wrongAnswerSFX = mixer.Sound(resourcePath("./sound/wrong-answer.mp3"))
        # self.suggestionAnswerSFX = mixer.Sound(resourcePath("./sound/suggestion-answer.mp3"))

        self.text = self["text"][3:].strip()

        self.imagePath = resourcePath("./img/answerFrame.png")
        self.resizeButtonImage(300, 50)
        self.config(bg=self.defaultBackground, font=("Segoe UI", 9, "bold"), border=0, relief='flat',
                    compound='center', disabledforeground='black', padx=10, pady=10)

    def changeNormalColor(self):
        self.setButtonImage(resourcePath("./img/answerFrame.png"))
        self.resizeButtonImage(300, 50)

    def changeSelectionColor(self):
        self.setButtonImage(resourcePath("./img/answerSelection.png"))
        self.resizeButtonImage(300, 50)

    def changeCorrectColor(self):
        self.setButtonImage(resourcePath("./img/answerCorrect.png"))
        self.resizeButtonImage(300, 50)

    def changeWrongColor(self):
        self.setButtonImage(resourcePath("./img/answerWrong.png"))
        self.resizeButtonImage(300, 50)

    def changeSuggestionColor(self):
        self.setButtonImage(resourcePath("./img/answerSuggestion.png"))
        self.resizeButtonImage(300, 50)

    def disable(self, hide: bool = False):
        super().disable()
        if hide:
            self.setButtonImage(resourcePath("./img/answerRemoved.png"))
            self.resizeButtonImage(300, 50)
            self['fg'] = 'black'


class ALifelineButton(AButton):
    def __init__(self, master, imgPath: str = None, callback=None, **kw):
        super().__init__(master, imgPath=imgPath, callback=callback, **kw)
        self.config(text='', compound='c', bg=self.defaultBackground, border=0, relief='flat', command=None)
        self["width"] = 116
        self["height"] = 86
        self.setButtonImage(self.imagePath)


class ALabel(Label):
    def __init__(self, master: Misc | None = ..., imgPath: str | None = ..., **kw):
        super().__init__(master, **kw)
        self.imgPath = imgPath
        self.setLabelImage(self.imgPath)

    def setLabelImage(self, path: str):
        self.imagePath = path
        self.labelImage = Image.open(self.imagePath)
        self.labelImage = ImageTk.PhotoImage(self.labelImage.resize((100, 50), Image.ANTIALIAS))
        self.config(image=self.labelImage)


class Timer(ALabel):
    def __init__(self, master: Misc | None = ..., imgPath: str | None = ..., **kw):
        super().__init__(master, imgPath=imgPath, **kw)
        self.config(bg='black', fg='white', compound='center', font=('sans-serif', 12, 'bold'))

    def changeToNormal(self):
        self.setLabelImage(resourcePath('./img/clockNormal.png'))

    def changeToLow(self):
        self.setLabelImage(resourcePath('./img/clockLow.png'))

    def changeToCritical(self):
        self.setLabelImage(resourcePath('./img/clockCritical.png'))


class LifeIcon(Label):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        self.imagePath = resourcePath('./img/heart.png')
        self.image = Image.open(self.imagePath)
        self.resizeButtonImage(32, 28)

    def resizeButtonImage(self, width=0, height=0):
        if not width == height == 0:
            self.image = self.image.resize((width, height), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.image)
        self.config(image=self.image)

    def setButtonImage(self, path: str):
        self.imagePath = path
        self.image = Image.open(self.imagePath)
        self.resizeButtonImage(32, 28)

    def disable(self):
        self.imagePath = resourcePath('./img/heartGray.png')
        self.image = Image.open(self.imagePath)
        self.resizeButtonImage(32, 28)
