from tkinter import *
from Primitives import ATextEntry, AHoverButton


class UsernameInput(Frame):
    def __init__(self, master: Misc | None = ..., **kw) -> None:
        super().__init__(master, **kw)
        self["background"] = "black"
        self["padx"] = 32
        self["pady"] = 16
        self.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.textPrompt = Label(
            self, background="black", foreground="white", text="Enter your name"
        )
        self.textPrompt.pack()

        self.username = StringVar(value="Player")
        self.entry = ATextEntry(
            self, background="white", relief="flat", textvariable=self.username
        )
        self.entry.pack(side=TOP, anchor=N)

        self.okButton = AHoverButton(
            self,
            background="#202169",
            foreground="white",
            border=0,
            width=10,
            command=self.okHandler,
            text="OK",
        )
        self.okButton.pack(side=TOP, anchor=N, pady=30)

    def okHandler(self) -> None:
        ...
