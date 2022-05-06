from multiprocessing.spawn import import_main_path
from tkinter import *
from dbAPI import getRandomQuestion
from numpy.random import shuffle
from time import time


class AView(Frame):
    ...


class Controller:
    def __init__(self) -> None:
        ...


class QuestionController(Controller):
    def __init__(self) -> None:
        super().__init__()
        questionInfo = getRandomQuestion()
        self.questionText = questionInfo["text"]
        self.correctAnswer = questionInfo["correct"]
        self.wrongAnswers = questionInfo["wrong"]
        self.shuffledAnswers = []
        self.shuffledAnswers.append(self.correctAnswer)
        for answer in self.wrongAnswers.values():
            self.shuffledAnswers.append(answer)
        shuffle(self.shuffledAnswers)

        self.timeStart = time()
        print(self.timeStart)

    def getNextAnswer(self) -> str:
        for answer in self.shuffledAnswers:
            yield answer


class MainWindow(Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Window Title")
        self.geometry("800x600+0+0")
        self["bg"] = "black"
        self.currentView = None

    def setView(self, view: AView = None):
        self.currentView = view
        self.currentView.pack()


class AView(Frame):
    def __init__(self, master: Misc | None = ..., **kw) -> None:
        super().__init__(master, **kw)

    @classmethod
    def fromFrame(cls):
        ...


class GameView(AView):
    def __init__(self, master: Misc | None = ..., **kw) -> None:
        super().__init__(master, **kw)
        self["bg"] = "yellow"
        self.questionFrame = QuestionFrame(master=self)
        self.questionFrame.pack()


class QuestionFrame(Frame):
    def __init__(self, master: Misc | None = ..., **kw) -> None:
        super().__init__(master, **kw)
        self.questionController = QuestionController()
        self.questionText = Label(
            master=self,
            text=self.questionController.questionText,
            font=("SegoeUI", 20, "bold"),
            bg="red",
        )
        self.questionText.pack()
        self.answerFrame = Frame(self)
        self.answerFrame.pack()
        self.answers = [AAnswerButton] * 4
        for index, answerText in enumerate(self.questionController.getNextAnswer()):
            self.answers[index] = AAnswerButton(
                master=self.answerFrame, index=index, controller=self.questionController, text=answerText
            )
            self.answers[index].grid(row=index // 2, column=index % 2, padx=10, pady=10)



class AButton(Button):
    def __init__(self, master: Misc | None = ..., controller: QuestionController = None, **kw) -> None:
        super().__init__(master, **kw)
        self.controller = controller
        self.text = self["text"]


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
        self["text"] = self["text"] + " MB"


class AAnswerButton(AButton):
    __textPrefix = ["A. ", "B. ", "Γ. ", "Δ. "]

    def __init__(self, master: Misc | None = ..., index: int = -1, **kw) -> None:
        super().__init__(master, **kw)
        self["bg"] = "green"
        if index >= 0:
            self["text"] = AAnswerButton.__textPrefix[index] + self["text"]
        else:
            self["text"] = self["text"]
        self['command'] = self.answerHandler

    def answerHandler(self) -> None:
        if self.controller.correctAnswer == self.text:
            print('Selected the CORRECT answer')
        else:
            print('Selected the WRONG answer')



class ALifelineButton(AButton):
    def __init__(self, master: Misc | None = ..., **kw) -> None:
        super().__init__(master, **kw)
        self["bg"] = "blue"
        self["text"] = self["text"] + " LB"


mainWindow = MainWindow()

mainWindow.setView(GameView(mainWindow))

mainWindow.mainloop()
