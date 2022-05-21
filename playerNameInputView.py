from tkinter import *
from PIL import Image, ImageTk
from filePath import resourcePath


class PlayerNameInputView(Frame):
    def __init__(self, master: Misc | None = ..., controller=None, **kw) -> None:
        super().__init__(master=master, **kw)
        self.controller = controller
        self.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.config(bg='black')

        self.message = Label(self, text='Enter your name')
        self.message.config(font=('Arial', 30, 'bold'), fg='white', bg='black', justify='center')
        self.message.pack(pady=20)

        self.playerNameEntry = Entry(self, textvariable=self.controller.playerName)
        self.playerNameEntry.config(font=('Arial', 24, 'bold'), justify='center')
        self.playerNameEntry.config(bg='blue', fg='white', relief='flat')
        self.playerNameEntry.config(highlightthickness=2, highlightbackground='aqua', highlightcolor='white')

        self.playerNameEntry.pack()

        self.debugButton = Button(self, text='Start Game', command=self.startGame())
        self.debugButton.pack(pady=20)

    def startGame(self):
        return self.controller.startHandler
