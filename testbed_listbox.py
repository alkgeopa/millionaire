from random import choice
from tkinter import *
from tinydb import *
import platform


# GUI stuff

win = Tk()

win.title('Επεξεργασία ερωτήσεων - ΠΘΝΓΕ')

win.geometry('800x600')

win.minsize(width=200, height=200)

defColor = '#ddd'

# Left frame for the questions
frameLeft = Frame(win, bg=defColor, width=300, borderwidth=1, padx=16)
frameLeft.pack(side=LEFT, fill=Y)

# Right frame for the options
frameRight = Frame(win, bg=defColor, width=500, borderwidth=1, padx=16)
frameRight.pack(side=LEFT, fill=BOTH, expand=1)

# Container for the options
labelFrameRight = LabelFrame(
    frameRight, bg=defColor, padx=10, pady=10, text='Επιλογές')
labelFrameRight.pack_propagate(False)
labelFrameRight.pack(side=TOP, fill=BOTH, expand=1, pady=(0, 16))

# Container for the question list and the scrollbar
labelFrameLeft = LabelFrame(
    frameLeft, bg=defColor, width=250, text='Ερωτήσεις', padx=10, pady=10)
labelFrameLeft.pack_propagate(False)
labelFrameLeft.pack(side=TOP, fill=Y, expand=1, pady=(0, 16))


class ListOption:
    def __init__(self) -> None:
        self.difficultyText = choice(['Ε', 'Μ', 'Δ'])
        self.questionText = 'Ποιο είναι το υψηλότερο βουνό της Ελλάδας;'

    def __str__(self) -> str:
        text = ' N{} - {}'
        return text.format(self.difficultyText, self.questionText)


class AScrollableList(Frame):
    def __init__(self, root) -> None:
        Frame.__init__(self, root)

        self.scrollList = Listbox(self, selectbackground='#00f',
                                  selectmode=SINGLE, relief=SOLID, borderwidth=0, border=0, font='Consolas', bd=0)
        self.scrollList.pack(side=TOP, anchor=NW, fill=BOTH, expand=TRUE)

        for row in range(10000):
            option = ListOption()
            self.scrollList.insert(END, option)


AScrollableList(labelFrameLeft).pack(side=TOP, fill=BOTH, expand=TRUE)

win.mainloop()
