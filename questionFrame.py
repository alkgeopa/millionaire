from widgets import *


class QuestionFrame(Frame):
    def __init__(self, master: Misc | None = ..., controller=None, **kw) -> None:
        super().__init__(master=master, **kw)
        self.questionController = controller
        self.pack(side=RIGHT, anchor=E, expand=1, fill=X)
        # # Το root για τα widgets του QuestionFrame είναι το `self`
        #
        # # Παρέχεται μια τυχαία ερώτηση κάθε φορά που τρέχει το παιχνίδι
        #
        # # Την ερώτηση την παίρνουμε από το self.questionController.questionText
        #
        # # Τις απαντήσεις από τη λίστα self.questionController.shuffledAnswers
        #   η από τον generator self.questionController.getNextQuestion()
        #
        # # Η σωστή απάντηση δίνεται στο self.questionController.correctAnswer
        #
        # # Για τις απαντήσεις χρησιμοποιούμε AAnswerButton αντί για Button
        #
        # # Στο AAnswerButton βάζουμε ένα όρισμα callback=self.questionController.checkAnswer
        #   για να μας ελέγξει αν η απάντηση που πατήσαμε είναι σωστή (προς το παρόν απλά το δείχνει στην κονσόλα)
        #
        # # Καλό είναι τα AAnswerButton να μπουν σε μια λίστα
        #
        # # Καλό είναι τα AAnswerButton να προβάλλονται με .grid()
        #
        #
        #
        # Από εδώ αρχίζουμε να γράφουμε
        self["background"] = "black"

        self.infoFrame = Frame(self)
        self.infoFrame.pack()

        self.lifesFrame = Frame(self.infoFrame)
        self.lifesFrame.pack(pady=10)
        # # self.numLives = self.questionController.gameController.livesVar.get()
        # self.lives = []
        # for i in range(self.questionController.gameController.maxLives):
        #     if i < self.questionController.gameController.lives:
        #         self.lives.append(LifeIcon(self.lifesFrame))

        #     else:
        #         self.lives.append(LifeIcon(self.lifesFrame))
        #         self.lives[-1].setButtonImage(resourcePath('./img/heartGray.png'))

        # self.lives[-1].pack(side=LEFT, anchor=E)
        
        self.lifesLabel = Label(self.lifesFrame, text='Lives:')
        self.lifesLabel.grid(row=0, column=0)
        self.lifesNum = Label(self.lifesFrame, textvariable=self.questionController.gameController.livesVar)
        self.lifesNum.grid(row=0, column=1)

        self.timerFrame = Frame(self.infoFrame)
        self.timerFrame.pack(pady=10)
        self.timerLabel = Label(self.timerFrame, text='Timer:')
        self.timerLabel.grid(row=0, column=0)
        self.timerNum = Label(self.timerFrame, textvariable=self.questionController.timerVar)
        self.timerNum.grid(row=0, column=1)
        self.questionController.updateTimer()

        self.questionText = Label(
            self,
            text=self.questionController.questionText,
            font=('sans-serif', 12, 'bold'),
            wraplength=600
        )
        self.questionText.pack()
        self.answersFrame = Frame(self, bg='black')
        self.answersFrame.pack()
        self.answersFrame.rowconfigure((0, 1), minsize=ANSWERHEIGHT + 10)
        self.answersFrame.columnconfigure((0, 1), minsize=ANSWERWIDTH + 10)
        self.answers: list[AAnswerButton] = [None] * 4
        for index, answer in enumerate(self.questionController.getNextAnswer()):
            self.answers[index] = AAnswerButton(
                self.answersFrame,
                text=f"{AAnswerButton.textPrefix[index]}{answer}",
                callback=self.questionController.checkAnswer,
            )
            self.answers[index].grid(row=index // 2, column=index % 2, pady=10, padx=10)
