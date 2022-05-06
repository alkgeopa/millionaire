from tkinter import *


class PlayerNameInputView(Frame):
    def __init__(self, master: Misc | None = ..., controller=None, **kw) -> None:
        super().__init__(master=master, **kw)
        self.controller = controller
        self.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.message = Label(self, text='Enter your name (input whatever or leave it as is, doesn\'t work anyway 😅 )')
        self.message.pack(pady=20)
        self.playerName = StringVar()
        self.playerNameEntry = Entry(self, textvariable=self.playerName)
        self.playerNameEntry.pack()
        self.debugButton = Button(self, text='Start Game', command=self.startGame())
        self.debugButton.pack(pady=20)

    def startGame(self):
        return lambda: self.controller.startHandler(self.playerName.get())
