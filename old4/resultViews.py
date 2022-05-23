from tkinter import Frame, Label, Button, Misc


class EndGameFrame(Frame):
    def __init__(self, master: Misc | None = ..., controller=None, **kw) -> None:
        super().__init__(master=master, **kw)

        self.gameController = controller

        self.pack(side='top', anchor='n', expand=1, fill='both')

        self.messageFrame = Frame(master=self)
        self.messageFrame.place(relx=0.5, rely=0.5, anchor='center')

        self.title = Label(master=self.messageFrame, text='', justify='center')

        self.amountWon = Label(master=self.messageFrame, justify='center')

        self.level = Label(master=self.messageFrame, justify='center')

        self.backToMenu = Button(master=self.messageFrame, text='Back to menu', command=self.gameController.mainMenuView)


class VictoryView(EndGameFrame):
    def __init__(self, master: Misc | None = ..., controller=None, **kw) -> None:
        super().__init__(master=master, controller=controller, **kw)

        self.config(bg='green')
        self.title.config(text='Congratulations, you have won!')
        self.title.pack(side='top', anchor='n')
        self.amountWon.config(textvariable=self.gameController.amountWon)
        self.amountWon.pack(side='top', anchor='n')
        self.backToMenu.pack(side='top', anchor='n')


class DefeatView(EndGameFrame):
    def __init__(self, master: Misc | None = ..., controller=None, **kw) -> None:
        super().__init__(master=master, controller=controller, **kw)

        self.config(bg='red')
        self.title.config(text='You have lost! Try again next time.')
        self.title.pack(side='top', anchor='n')
        self.level.config(text=f'You have made it to question {self.gameController.level + 1}.')
        self.level.pack(side='top', anchor='n')
        self.backToMenu.pack(side='top', anchor='n')
