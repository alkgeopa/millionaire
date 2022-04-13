from tkinter import *
from PIL import Image, ImageTk
from pygame import mixer
from Controller import GameController


class ATextEntry(Entry):
    def __init__(self, master, **kw) -> None:
        super().__init__(master=master, **kw)


class AHoverButton(Button):
    def __init__(self, master, **kw) -> None:
        super().__init__(master=master, **kw)
        self.defaultBackground = self['background']
        self.defaultForeground = self['foreground']
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']
        self['foreground'] = self['activeforeground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground
        self['foreground'] = self.defaultForeground


class AImageButton(Button):
    def __init__(self, master: Misc | None = ..., **kw) -> None:
        super().__init__(master, **kw)
        self.buttonImage: Image = None


        self.defaultBackground = 'black'
        self.defaultForeground = 'white'
        self['background'] = self.defaultBackground
        self['foreground'] = self.defaultForeground
        self['activebackground'] = self.defaultBackground
        self['activeforeground'] = self.defaultForeground

    def initImage(self, path: str) -> ImageTk.PhotoImage:
        '''
        Prepares and returns the buttons image
        '''
        img = Image.open(path)
        # img = img.resize((67, 50), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        return img

    def setButtonImage(self, path: str):
        self.imagePath = path
        self.buttonImage = self.initImage(self.imagePath)
        self.config(image=self.buttonImage)

    def resizeButtonImage(self, width=0, height=0):
        if width == height == 0:
            return
        img = Image.open(self.imagePath)
        img = img.resize((width, height), Image.ANTIALIAS)
        self.buttonImage = ImageTk.PhotoImage(img)
        self.config(image=self.buttonImage)

    def getButtonText(self):
        return self.text




class ALifelineButton(AImageButton):
    def __init__(self, master: Misc | None = ..., **kw) -> None:
        super().__init__(master, **kw)

        self.text: str = self['text']
        self['text'] = ''
        self.bind('1>', self.clickHandler)


    def clickHandler(self, event: Event=None):
        if self.text in GameController.availableLifelines.keys():
            GameController.lifelineHandler(self.text)
            self.destroy()




class AAnswerButton(AImageButton):
    def __init__(self, master: Misc | None = ..., controller: Misc | None = ..., **kw) -> None:
        super().__init__(master, **kw)

        self.finalAnswerSFX = mixer.Sound('./sound/final-answer.mp3')
        self.correctAnswerSFX = mixer.Sound('./sound/correct-answer.mp3')
        self.wrongAnswerSFX = mixer.Sound('./sound/wrong-answer.mp3')
        self.suggestionAnswerSFX = mixer.Sound('./sound/suggestion-answer.mp3')

        self.text = self['text'][3:].strip()

        self.setButtonImage('./img/answerFrame.png')
        self.resizeButtonImage(300, 50)
        self.defaultBackground = 'black'
        self.defaultForeground = 'white'
        self['background'] = self.defaultBackground
        self['foreground'] = self.defaultForeground
        self['activeforeground'] = self.defaultForeground
        self['activebackground'] = '#111'
        self['font']=('Segoe UI', 9, 'bold')
        self['pady'] = 10
        self['padx'] = 10
        self['border'] = 0
        self['relief'] = 'flat'
        self['compound'] = 'center'
        self.bind('<Enter>', self.onEnter)
        self.bind('<Leave>', self.onLeave)
        self.bind('<Button-1>', self.clickHandler)

    def onEnter(self, event: Event=None):
        self['background'] = '#111'

    def onLeave(self, event: Event=None):
        self['background'] = self.defaultBackground

    def unbindAll(self) -> None:
        self.unbind('<Enter>')
        self.unbind('<Leave>')

    def getAnswerText(self):
        return self.text

    def clickHandler(self, event: Event=None):
        print(event)
        GameController.printDebug()
        if not GameController.answerSelected:
            GameController.answerSelected = self.text
            print(f'answerSelected: {GameController.answerSelected}')
            self.setButtonImage('./img/answerSelection.png')
            self.resizeButtonImage(300, 50)


            self.finalAnswerSFX.play()
            self.finalAnswerSFX.set_volume(0.5)
            GameController.globalWindow.after(5000, self.readyChecks) #TODO DELETE
            GameController.globalWindow.after(5000, self.finalAnswerSFX.stop) #TODO DELETE


    def readyChecks(self):
        if GameController.checkAnswer():
            self.changeCorrectColor()
            GameController.globalWindow.after(4000, GameController.nextQuestion)
        else:
            self.changeWrongColor()
            GameController.lightCorrectAnswer()

    def changeCorrectColor(self, playSound=True):
        self.setButtonImage('./img/answerCorrect.png')
        self.resizeButtonImage(300, 50)

        if playSound:
            self.correctAnswerSFX.play(loops=0, fade_ms=100)
            self.correctAnswerSFX.set_volume(0.5)
            self.finalAnswerSFX.stop()
            GameController.globalWindow.after(3000, self.correctAnswerSFX.fadeout, 1500)

    def changeWrongColor(self):
        self.setButtonImage('./img/answerWrong.png')
        self.resizeButtonImage(300, 50)

        self.wrongAnswerSFX.play(loops=0, fade_ms=100)
        self.wrongAnswerSFX.set_volume(0.5)
        self.finalAnswerSFX.stop()

    def changeSuggestionColor(self):
        self.setButtonImage('./img/answerSuggestion.png')
        self.resizeButtonImage(300, 50)

        self.suggestionAnswerSFX.play(loops=0)
        self.suggestionAnswerSFX.set_volume(0.2)

    def changeBlackColor(self):
        self.setButtonImage('./img/answerRemoved.png')
        self.resizeButtonImage(300, 50)


class ATextFrame(Frame):
    def __init__(self, master: Misc | None = ..., **kw) -> None:
        super().__init__(master=master, **kw)



    def initBackgroundImage(self, path: str) -> ImageTk.PhotoImage:
        ...

    def setBackgroundImage(self, path: str) -> None:
        ...


