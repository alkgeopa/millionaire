from turtle import width
from Primitives import *
from PIL import ImageTk, Image


class GameLevel:
    def __init__(self, root: Tk) -> None:
        self.root = root
        self.questionPanel = QuestionPanel(self.root, background='yellow', height=100, width=100)
        self.questionPanel.pack()


class QuestionPanel(Frame):
    '''
    Extends Tk.Frame class
    '''
    def __init__(self, master: Misc | None = ..., **kw) -> None:
        super().__init__(master=master, **kw)

        self.img = self.initImage()
        self.logo = Label(self, image=self.img, background='black')
        self.logo.pack(side=TOP, anchor=N)

        self.questionTextFrame = Frame(self, background='yellow')
        self.questionTextFrame.pack(side=TOP, anchor=N)
        questionFont = ('Segoe UI', 12)
        self.questionText = Label(
            self.questionTextFrame,
            font=questionFont,
            background='#010541',
            foreground='white',
            bd=0,
            text='HERE GOES THE QUESTION TEXT'
        )
        self.questionText.pack(padx=1, pady=1)

        self.answersFrame = Frame(self)
        self.answersFrame.pack(side=TOP, anchor=N)

        self.answer1 = AAnswerButton(self.answersFrame, text='Α. ' + 'Answer 1')
        self.answer1.grid(row=0, column=0, padx=20, pady=20)

        self.answer2 = AAnswerButton(self.answersFrame, text='Β. ' + 'Answer 1')
        self.answer2.grid(row=0, column=1, padx=20, pady=20)

        self.answer3 = AAnswerButton(self.answersFrame, text='Γ. ' + 'Answer 1')
        self.answer3.grid(row=1, column=0, padx=20, pady=20)

        self.answer4 = AAnswerButton(self.answersFrame, text='Δ. ' + 'Answer 1')
        self.answer4.grid(row=1, column=1, padx=20, pady=20)


    def initImage(self) -> ImageTk.PhotoImage:
        '''
        Prepares and returns the logo image
        '''
        img = Image.open('./img/logo.png')
        img = img.resize((250, 250), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        return img


class SidePanel(Frame):
    pass
