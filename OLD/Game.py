from PIL import ImageTk, Image
from pygame import mixer
from Controller import GameController
from Primitives import *
from dbAPI import *


class GameLevel:
    def __init__(self, root: Tk) -> None:
        self.root = root
        GameController.initGameController(window=self.root)
        GameController.replaceQuestion = self.replaceQuestion
        GameController.goToNextQuestion = self.nextQuestion
        # self.question = GameController.getQuestion() //DELETE
        self.questionPanel = QuestionPanel(self.root, background='black', height=200, width=200)
        self.questionPanel.pack(side=RIGHT, anchor=E, expand=1, fill=X)
        self.sidePanel = SidePanel(self.root, background='black', width=500)
        self.sidePanel.pack(side=LEFT, anchor=W)

    def runLevel(self):
        pass

    def replaceQuestion(self):
        self.questionPanel.destroy()
        self.questionPanel = QuestionPanel(self.root, background='black', height=200, width=200)
        self.questionPanel.pack(side=RIGHT, anchor=E, expand=1, fill=X)

    def nextQuestion(self):
        self.sidePanel.destroy()
        self.sidePanel = SidePanel(self.root, background='black', width=500)
        self.sidePanel.pack(side=LEFT, anchor=W)
        self.replaceQuestion()




class QuestionPanel(Frame):
    '''
    Extends ``Tk.Frame`` class
    '''
    def __init__(self, master: Misc | None = ..., **kw) -> None:
        super().__init__(master=master, **kw)

        # Get question from th
        self.question = GameController.getQuestion()
        self.answers = []
        self.answers.append(self.question['correct'])
        for w in self.question['wrong']:
            self.answers.append(self.question['wrong'][w])
        shuffle(self.answers)

        self.img = self.initImage()
        self.logo = Label(self, image=self.img, background='black')
        self.logo.pack(side=TOP, anchor=N)

        self.questionTextFrame = Frame(self, background='black')
        self.questionTextFrame.pack(side=TOP, anchor=N, expand=1, fill=X, pady=20)
        questionFont = ('Segoe UI', 12)
        self.questionText = Label(
            self.questionTextFrame,
            font=questionFont,
            background='black',
            foreground='white',
            bd=0,
            pady=20,
            text=self.question['text']
        )
        self.questionText.pack(padx=1, pady=1)

        self.answersFrame = Frame(self, background='black')
        self.answersFrame.pack(side=TOP, anchor=N)

        self.answer1 = AAnswerButton(self.answersFrame, controller=GameController, text='Α.  ' + self.answers[0])
        self.answer1.grid(row=0, column=0, padx=20, pady=20)

        self.answer2 = AAnswerButton(self.answersFrame, text='Β.  ' + self.answers[1])
        self.answer2.grid(row=0, column=1, padx=20, pady=20)

        self.answer3 = AAnswerButton(self.answersFrame, text='Γ.  ' + self.answers[2])
        self.answer3.grid(row=1, column=0, padx=20, pady=20)

        self.answer4 = AAnswerButton(self.answersFrame, text='Δ.  ' + self.answers[3])
        self.answer4.grid(row=1, column=1, padx=20, pady=20)



        GameController.answerWidgets = [
            self.answer1,
            self.answer2,
            self.answer3,
            self.answer4,
        ]


    def initImage(self) -> ImageTk.PhotoImage:
        '''
        Prepares and returns the logo image
        '''
        img = Image.open('./img/logo.png')
        img = img.resize((250, 250), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        return img


class SidePanel(Frame):

    ammounts = [
        '100',
        '200',
        '300',
        '500',
        '1.000',
        '1.500',
        '2.000',
        '3.500',
        '5.000',
        '7.500',
        '10.000',
        '20.000',
        '50.000',
        '100.000',
        '250.000'
    ]

    def __init__(self, master: Misc | None = ..., **kw) -> None:
        super().__init__(master=master, **kw)

        # Create lifelines' frame
        self.lifelinesFrame = Frame(self, background='black')
        self.lifelinesFrame.pack(side=TOP, pady=30, expand=1, fill=X)
        self.lifelines: list[ALifelineButton] = []
        for index, lifeline in enumerate(GameController.availableLifelines.keys()):


            lline = ALifelineButton(self.lifelinesFrame, text=lifeline)

            self.lifelines.append(lline)

            self.lifelines[index].setButtonImage(f'./img/{lifeline}.png')

            self.lifelines[index].grid(row=0, column=index, padx=12)



            GameController.availableLifelines[lifeline] = lline
            print(GameController.availableLifelines[lifeline].text)


        # Create amounts' list
        self.questionLevelsFrame = Frame(self, background='black')
        self.questionLevelsFrame.pack(side=BOTTOM, expand=1, fill=X)
        self.questionLevels: list[Label] = []
        for index, level in enumerate(SidePanel.ammounts):
            if level=='1.000' or level=='7.500':
                self.questionLevels.append(
                    Label(
                        self.questionLevelsFrame,
                        width=25,
                        pady=1,
                        font='Arial 20 bold underline',
                        foreground='grey',
                        background='black',
                        text=f'{str(index+1)}   {level} €'
                    )
                )
            else:
                self.questionLevels.append(
                    Label(
                        self.questionLevelsFrame,
                        width=25,
                        pady=1,
                        font='Arial 20 bold',
                        foreground='grey',
                        background='black',
                        text=f'{str(index+1)}   {level} €'
                    )
                )
            self.questionLevels[index].pack(side=BOTTOM, anchor=S)

        self.highlightCurrentAmmount(GameController.currentQuestion)

    def highlightCurrentAmmount(self, index) -> None:
        self.questionLevels[index].config(foreground='black', background='#ffb51e')


class VictoryFrame(Frame):
    def __init__(self, master: Misc | None = ..., **kw) -> None:
        super().__init__(master=master, **kw)

        self.title = Label(
            self,
            background='black',
            foreground='white',
            font=('Segoe UI', 30,
            'bold'),
            text='{PLAYERNAME}, you won!'
        )
        self.title.pack(side=TOP, anchor=N)

        self.wonAmount = Label(
            self,
            background='black',
            foreground='yellow',
            font=('Segoe UI', 36,
            'bold'),
            text='💶 {AMOUNT} € 💶'
        )
