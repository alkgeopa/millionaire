import random
from tkinter import *
from tinydb import *


# GUI stuff

win = Tk()

win.title('Επεξεργασία ερωτήσεων - ΠΘΝΓΕ')

win.geometry('800x600')

win.minsize(width=200, height=200)

defColor = '#ddd'

# TODO
# Scrollbars
scrollbarVertical = Scrollbar(win)
scrollbarVertical.pack(side=RIGHT, fill=Y)
scrollbarHorizontal = Scrollbar(win, orient=HORIZONTAL)
scrollbarHorizontal.pack(side=BOTTOM, fill=X)

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

'''
# Container for the question list
frameInnerScrollable = Canvas(labelFrameLeft, bg=defColor, width=200)
frameInnerScrollable.pack_propagate(False)
frameInnerScrollable.pack(side=LEFT, fill=Y, expand=0)

# Scrollbar for the question list
scrollbarLeftInnerVertical = Scrollbar(labelFrameLeft, orient=VERTICAL, command=frameInnerScrollable.yview)
scrollbarLeftInnerVertical.pack(side=RIGHT, fill=Y)

frameInnerScrollable.configure(yscrollcommand=scrollbarLeftInnerVertical.set)

# Container for a single question
frameQuestionSelect = Frame(frameInnerScrollable, bg='#855', width=250)
frameQuestionSelect.pack(side=TOP, anchor=N, fill=None, expand=0)

# Difficulty Label
difficultyLevelLabel = Label(
    frameQuestionSelect, bg=defColor, borderwidth=0, text='E', padx=16)
difficultyLevelLabel.grid(row=0, column=0, columnspan=3)

# Question title
questionLabel = Label(frameQuestionSelect, bg='#ff5',
                      text='Ποιο είναι το υψόμετρο της κορυφής «Μύτικας», της υψηλοτερη κορυφής του Ολύμπου;')
questionLabel.grid(row=0, column=3, columnspan=4)

questionLabelList = list()

for question in range(50):
    color = ["#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])]
    question = Frame(frameInnerScrollable, bg=color, width=250, height=20)
    question.pack(side=TOP, anchor=N, fill=None, expand=0)
'''

class ALabelFrame(LabelFrame):
    '''
    Custon LabelFrame
    '''
    pass


win.mainloop()
