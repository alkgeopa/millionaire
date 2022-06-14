from __future__ import annotations

from tkinter import Misc, Frame, Label
from typing import TYPE_CHECKING

from PIL import Image, ImageTk

from filePath import resourcePath
from widgets import AAnswerButton

if TYPE_CHECKING:
    from controller import QuestionController


class QuestionFrame(Frame):
    """Based on the tkinter frame. Acts as a container for the question-related widgets"""

    def __init__(self, master: Misc | None = ..., controller: QuestionController | None = ..., **kw) -> None:
        super().__init__(master=master, **kw)
        self.questionController = controller
        self.pack(side='right', anchor='e', expand=1, fill='both')
        self.questionController.updateTimer()
        self['background'] = 'black'

        # millionaire frame
        self.millionaire_frame = Frame(master=self, width=480, height=250, bg="black")
        self.millionaire_frame.grid(row=0, column=1)

        # εμφάνιση κεντρικής εικόνας Εκατομμυριούχος
        millionaire_img = Image.open(resourcePath("img/millionaire.png"))
        millionaire_img = millionaire_img.resize((400, 380), Image.ANTIALIAS)
        self.millionaire_img = ImageTk.PhotoImage(millionaire_img)
        self.millionaire = Label(self.millionaire_frame, bg="black", image=self.millionaire_img, )
        self.millionaire.grid(row=0, column=1)

        # player_time frame
        self.player_time_frame = Frame(master=self, width=480, height=100, bg="black")
        self.player_time_frame.grid(row=1, column=1)

        self.name = Label(self.player_time_frame, bg="black", font=('times new roman', 11, 'bold'), fg='white', bd=5,
                          height=2, text=f'{"Player: "} {self.questionController.playerName.get()}')
        self.name.grid(row=0, column=0)

        self.lives = Label(self.player_time_frame, bg="black", font=('times new roman', 11, 'bold'), fg='white',
                           text=f'{"Lives: "}{self.questionController.gameController.livesVar.get()}', )
        self.lives.grid(row=1, column=0, sticky='nw')

        self.timer = Label(self.player_time_frame, bg="black", font=('times new roman', 11, 'bold'), fg='white',
                           textvariable=self.questionController.timer)
        self.timer.grid(row=1, column=1)

        # question frame
        self.question_frame = Frame(master=self, width=480, height=250, bg="black")
        self.question_frame.grid(row=2, column=1)

        self.question = Label(self.question_frame, bg="black", font=('times new roman', 11, 'bold'), fg='white', bd=5,
                              height=2, width=60, justify='center', text=self.questionController.questionText,
                              wraplength=500)
        self.question.grid(row=0, column=0, columnspan=4, pady=4)

        self.answer = []
        for i in range(4):
            button = AAnswerButton(self.question_frame, bg="black", fg="white",
                                   text=f'{AAnswerButton.textPrefix[i]} {self.questionController.shuffledAnswers[i]}',
                                   callback=self.questionController.checkAnswer)
            self.answer.append(button)
        # self.answer[i].grid(row=i//2, column=i%2)

        self.answer[0].grid(row=1, column=1)
        self.answer[1].grid(row=1, column=3)
        self.answer[2].grid(row=2, column=1)
        self.answer[3].grid(row=2, column=3)
