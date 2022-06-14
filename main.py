from tkinter import Tk

from controller import ApplicationController
from filePath import resourcePath


class App(Tk):
    """Main app class"""

    def __init__(self) -> None:
        super().__init__()
        self.title("ΠΟΙΟΣ ΘΕΛΕΙ ΝΑ ΓΙΝΕΙ ΕΚΑΤΟΜΜΥΡΙΟΥΧΟΣ")
        self.iconbitmap(resourcePath('img/icon.ico'))
        self.geometry("1000x700+0+0")
        self["bg"] = "black"
        self.appController = ApplicationController(self)


def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
