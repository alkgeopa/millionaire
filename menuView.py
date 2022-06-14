from tkinter import Misc, Frame, Label

from widgets import AMenuButton


class MainMenu(Frame):
    """View & container for the main menu"""

    def __init__(self, master: Misc | None = ..., controller=None, **kw) -> None:
        super().__init__(master=master, **kw)
        self.controller = controller
        self['background'] = 'black'
        self.place(relx=0.5, rely=0.5, anchor='center')
        self.title = Label(self, text='ΠΟΙΟΣ ΘΕΛΕΙ ΝΑ ΓΙΝΕΙ ΕΚΑΤΟΜΜΥΡΙΟΥΧΟΣ', font=('san-serif', 40, 'bold'),
                           bg='black', fg='white', wraplength=600)
        self.title.pack()
        self.btnStart = AMenuButton(master=self, text='Start', font=('san-serif', 20, 'bold'), width=10, height=1,
                                    command=self.startHandler())
        self.btnStart.pack(pady=20)
        self.btnTopTen = AMenuButton(master=self, text='Top 10', font=('san-serif', 20, 'bold'), width=10, height=1,
                                     command=self.topTenHandler())
        self.btnTopTen.pack(pady=20)
        self.btnExit = AMenuButton(master=self, text='Exit', font=('san-serif', 20, 'bold'), width=10, height=1,
                                   command=master.quit)
        self.btnExit.pack(pady=20)

    def startHandler(self):
        return self.controller.startHandler

    def topTenHandler(self):
        return self.controller.topTenHandler
