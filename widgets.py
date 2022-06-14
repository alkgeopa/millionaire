from tkinter import Misc, Button

from PIL import Image, ImageTk

from filePath import resourcePath


class AButton(Button):
    """Base class for buttons. Build for extendability"""

    def __init__(self, master: Misc | None = ..., **kw) -> None:
        super().__init__(master, **kw)
        self.text = self["text"]


class AMenuButton(AButton):
    """Menu button variant"""

    def __init__(self, master: Misc | None = ..., **kw) -> None:
        super().__init__(master, **kw)
        self['bg'] = 'purple'


class AAnswerButton(AButton):
    """Answer button variant"""
    textPrefix = ["A. ", "B. ", "Γ. ", "Δ. "]

    def __init__(self, master: Misc | None = ..., callback=None, **kw) -> None:
        super().__init__(master, **kw)
        self.text = self['text'][3:].strip()
        self.answer_img = None
        self.setImage("img/answerFrame.png")
        self['activebackground'] = 'black'
        self.bind('<1>', callback)

    def changeState(self):
        """Disables the button"""
        self.bind('<1>', lambda _: 'break')

    def setImage(self, path: str):
        """Sets the background image of the button"""
        answer_img = Image.open(resourcePath(path))
        answer_img = answer_img.resize((250, 60), Image.ANTIALIAS)
        self.answer_img = ImageTk.PhotoImage(answer_img)
        self.config(image=self.answer_img, compound="center", border=0, relief="flat")

    def changeToOrange(self):
        self.setImage("img/answerSelection.png")

    def changeToRed(self):
        self.setImage("img/answerWrong.png")

    def changeToGreen(self):
        self.setImage("img/answerCorrect.png")

    def changeToSuggestion(self):
        self.setImage("img/answerSuggestion.png")


class ALifelineButton(AButton):
    """Lifeline button variant"""

    def __init__(self, master: Misc | None = ..., imgPath=None, def_adress=None, **kw) -> None:
        super().__init__(master, **kw)
        self.text = self['text']
        self['text'] = ''
        self.config(bg='black', activebackground='black', relief='flat')

        self.imgPath = imgPath
        btnImg = Image.open(self.imgPath)
        btnImg = btnImg.resize((80, 60), Image.ANTIALIAS)
        self.btnImg = ImageTk.PhotoImage(btnImg)
        self.config(image=self.btnImg)

        self.LifeLineHandler = def_adress
        self.bind("<1>", self.LifeLineHandler)
