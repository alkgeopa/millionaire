from random import choice
from tkinter import *
from tkinter import ttk
from tinydb import *
import platform


db = TinyDB('db.json')
users = db.table('users')
questions = db.table('questions')
duplicateCheck = Query()

text = 'Ποιο είναι το υψηλότερο βουνό της Ελλάδας;'
if questions.search(duplicateCheck.text == text):
    print('Already in DB')
else:
    questions.insert({
        'text': text,
        'difficulty': 0,
        'correct': 'Όλυμπος',
        'wrong': {
            'w1': 'Ψηλορείτης',
            'w2': 'Σμόλικας',
            'w3': 'Παρνασσός',
        }
    })


class Question:
    def __init__(self, text: str, difficulty: int, correct: str, wrong1: str, wrong2: str, wrong3: str) -> int:
        if not (text or difficulty or correct or wrong1 or wrong2 or wrong3):
            return True
        else:
            pass






# GUI stuff

win = Tk()

win.title('Επεξεργασία ερωτήσεων - ΠΘΝΓΕ')

win.geometry('800x600')

win.minsize(width=200, height=200)

defColor = '#ddd'

panedWindow = PanedWindow(win, background='#aaa')
panedWindow.pack(side=TOP, fill=BOTH, expand=YES)

# Left frame for the questions
frameLeft = Frame(win, bg=defColor, width=400, borderwidth=1, padx=16)
frameLeft.pack(side=TOP, fill=Y)
panedWindow.add(frameLeft)

# Right frame for the options
frameRight = Frame(win, bg=defColor, width=500, borderwidth=1, padx=16)
frameRight.pack(side=LEFT, fill=BOTH, expand=1)
panedWindow.add(frameRight)

# Container for the options
labelFrameRight = LabelFrame(
    frameRight, bg=defColor, padx=10, pady=10, text='Επιλογές')
labelFrameRight.pack_propagate(False)
labelFrameRight.pack(side=TOP, fill=BOTH, expand=1, pady=(0, 16))

# # Container for the question list and the scrollbar
# labelFrameLeft = LabelFrame(
#     frameLeft, bg=defColor, width=350, text='Ερωτήσεις', padx=10, pady=10)
# labelFrameLeft.pack_propagate(False)
# labelFrameLeft.pack(side=TOP, fill=Y, expand=1, pady=(0, 16))


table = ttk.Treeview(frameLeft)
table['columns'] = ('id', 'difficulty', 'text')
table.column('#0', width=0, stretch=NO)
table.column('id', width=0, stretch=YES)
table.column('difficulty', anchor=NW, width=0, stretch=YES)
table.column('text', anchor=NW)

table.heading('#0', text='', anchor=W)
table.heading('id', text='ID', anchor=W)
table.heading('difficulty', text='Δυσκ.', anchor=W)
table.heading('text', text='Ερώτηση', anchor=W)

for i in range(100):
    table.insert(parent='', index=i, iid=i, text='', values=(
        str(i+10000000), choice(['Ε', 'Μ', 'Δ']), 'Ποιο είναι το υψηλότερο βουνό της Ελλάδας;'))

table.pack(side=BOTTOM, fill=BOTH, expand=YES, pady=(8, 16))


class OptionFrame():
    def __init__(self):
        self.frame = Frame(labelFrameRight, bg='blue')
        self.frame.pack(side=TOP, fill=BOTH, expand=YES)

def addNewButtonHandler():
    OptionFrame()

addNewButton = Button(frameLeft, text='Νέα ερώτηση', command=addNewButtonHandler)
addNewButton.pack(side=TOP, pady=(10,0))

win.mainloop()
