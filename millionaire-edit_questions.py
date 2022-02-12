from cmath import exp
from inspect import FrameInfo
from os import access
from tkinter import *
from tinydb import *


# GUI stuff

win = Tk()

win.title('Επεξεργασία ερωτήσεων - ΠΘΝΓΕ')

win.geometry('800x600')

# TODO
# Scrollbars
scrollbarVertical = Scrollbar(win)
scrollbarVertical.pack(side=RIGHT, fill=Y)
scrollbarHorizontal = Scrollbar(win, orient=HORIZONTAL)
scrollbarHorizontal.pack(side=BOTTOM, fill=X)

# Left frame for the questions
frameLeft = Frame(win, bg='#ccc', width=300, borderwidth=1, padx=16)
frameLeft.pack(side=LEFT, fill=Y)

# Right frame for the options
frameRight = Frame(win, bg='#aaa', width=500, border=1, padx=5, pady=5)
frameRight.pack(side=LEFT, fill=BOTH, expand=1)

# Title for frameLeft
frameLeftLabel = Label(frameLeft, text='Ερωτήσεις στη ΒΔ',
                       justify=LEFT, anchor=W, bg='#ddd', height=1)
frameLeftLabel.pack(side=TOP, fill=X, padx=(0, 82))

# Container for the question list and the scrollbar
frameLeftInner = Frame(frameLeft, bg='#eee', width=250)
frameLeftInner.pack(side=TOP, fill=BOTH, expand=1, pady=(0, 16))

# Scrollbar for the question list
scrollbarLeftInnerVertical = Scrollbar(frameLeftInner)
scrollbarLeftInnerVertical.pack(side=RIGHT, fill=Y)

# Container for the question list
frameInnerScrollable = Canvas(frameLeftInner, bg='#990', borderwidth=5, insertborderwidth=5)
frameInnerScrollable.pack(side=LEFT, fill=BOTH, expand=1)

# Container for a single question
frameQuestionSelect = Frame(frameInnerScrollable, bg='#855')
frameQuestionSelect.pack(side=TOP, anchor=N, fill=X, expand=1)

# Difficulty Label
difficultyLevelLabel = Label(frameQuestionSelect, bg='#585', text='E', padx=16)
difficultyLevelLabel.pack(side=LEFT)

# Question Label
questionLabel = Label(frameQuestionSelect, bg='#885', padx=8,
                      text='Ποιο είναι το υψόμετρο της κορυφής «Μύτικας», της υψηλοτερη κορυφής του Ολύμπου;')
questionLabel.pack(side=LEFT)


win.mainloop()
