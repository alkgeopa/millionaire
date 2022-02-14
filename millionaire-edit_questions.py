from random import choice
from tkinter import *
from tkinter import ttk
from tinydb import TinyDB, Query
import platform


db = TinyDB('db.json')
db.drop_tables()
users = db.table('users')
questions = db.table('questions')
dbQuery = Query()


def dummyData():
    return [
        {
            'text': 'Ποιο είναι το υψηλότερο βουνό της Ελλάδας;',
            'difficulty': 0,
            'correct': 'Όλυμπος',
            'wrong': {
                'w1': 'Ψηλορείτης',
                'w2': 'Σμόλικας',
                'w3': 'Παρνασσός',
            }
        },
        {
            'text': 'Ποιο είναι το υψος της κορυφής των Ιμαλαΐων, Έβερεστ;',
            'difficulty': 1,
            'correct': '8.849 μ.',
            'wrong': {
                'w1': '10.534 μ.',
                'w2': '5.948 μ.',
                'w3': '7.917 μ.',
            }
        },
        {
            'text': 'Ποιο είναι το βάθος της Τάφρου των Μαριανών',
            'difficulty': 2,
            'correct': '10.994 μ.',
            'wrong': {
                'w1': '11.275 μ.',
                'w2': '10.534 μ.',
                'w3': '11.103 μ.',
            }
        }
    ]


questions.insert_multiple(dummyData())


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
table.column('id', width=80, stretch=NO)
table.column('difficulty', anchor=NW, width=50, stretch=NO)
table.column('text', anchor=NW)

table.heading('#0', text='', anchor=W)
table.heading('id', text=' ID', anchor=W)
table.heading('difficulty', text=' Δυσκ.', anchor=W)
table.heading('text', text=' Ερώτηση', anchor=W)

allQuestions = questions.all()
for question in allQuestions:
    print(question.get('text'))
    table.insert(parent='', index=int(question.doc_id), iid=int(question.doc_id), values=(
        str(question.doc_id), question.get('difficulty'), question.get('text'))
    )

# for i in range(100):
#     table.insert(parent='', index=i, iid=i, text='', values=(
#         str(i+10000000), choice(['Ε', 'Μ', 'Δ']), 'Ποιο είναι το υψηλότερο βουνό της Ελλάδας;'))

table.pack(side=BOTTOM, fill=BOTH, expand=YES, pady=(8, 16))


class AnswerFrame:
    def __init__(self, parent, text, padx):
        self.frame = Frame(parent, pady=10)
        self.frame.pack(side=TOP, anchor=NW, fill=X)

        self.label = Label(self.frame, text=text, padx=padx)
        self.label.grid(row=0, column=0)

        self.text = Text(self.frame, height=1, width=30)
        self.text.grid(row=0, column=1)


class OptionFrame:

    state = {
        'open': False,
        'duplicate': False,
        'success': False,
        'currentFrame': None,
    }

    def __init__(self):

        self.frame = Frame(labelFrameRight, bg=defColor)
        self.frame.pack(side=TOP, fill=BOTH, expand=YES)

        self.panelText = LabelFrame(
            self.frame, height=100, bg=defColor, text='Κείμενο', padx=5, pady=5)
        self.panelText.pack(side=TOP, anchor=NW, fill=X)

        self.questionText = Text(self.panelText, height=4)
        self.questionText.pack(side=TOP, anchor=NW, fill=X)

        self.difficultyFrame = LabelFrame(
            self.frame, bg=defColor, text='Δυσκολία')
        self.difficultyFrame.pack(side=TOP, anchor=NW, fill=X)

        self.difficultySelelctions = [
            Radiobutton(self.difficultyFrame, text='Εύκολη',
                        justify=LEFT, value=0, variable='dif'),
            Radiobutton(self.difficultyFrame, text='Μέτρια',
                        justify=LEFT, value=1, variable='dif'),
            Radiobutton(self.difficultyFrame, text='Δύσκολη',
                        justify=LEFT, value=2, variable='dif')
        ]

        for selection in self.difficultySelelctions:
            selection.pack(side=LEFT, anchor=NW)
            selection.deselect()

        self.answerFrame = LabelFrame(
            self.frame, text='Απαντήσεις', bg=defColor)
        self.answerFrame.pack(side=TOP, anchor=NW, fill=X)

        self.correct = AnswerFrame(self.answerFrame, 'Σωστή', 22)
        self.wrong1 = AnswerFrame(self.answerFrame, 'Λάθος 1', 16)
        self.wrong2 = AnswerFrame(self.answerFrame, 'Λάθος 2', 16)
        self.wrong3 = AnswerFrame(self.answerFrame, 'Λάθος 3', 16)

        self.buttonGroup = Frame(self.frame, bg=defColor, pady=16)
        self.buttonGroup.pack(side=TOP, anchor=NW)

        self.saveBtn = Button(self.buttonGroup, text='Αποθήκευση')
        self.saveBtn.grid(row=0, column=0, padx=(0, 10))

        self.cancelBtn = Button(self.buttonGroup, text='Άκυρο')
        self.cancelBtn.grid(row=0, column=1, padx=(0, 10))

        self.saveBtn = Button(self.buttonGroup, text='Διαγραφή', bg='#eaa')
        self.saveBtn.grid(row=0, column=2, padx=(0, 10))

        OptionFrame.state['currentFrame'] = self.frame


def addNewButtonHandler():
    if not OptionFrame.state['open']:
        OptionFrame.state['open'] = True
        OptionFrame()
    else:
        OptionFrame.state['open'] = False
        for widget in labelFrameRight.pack_slaves():
            widget.destroy()


addNewButton = Button(frameLeft, text='Νέα ερώτηση',
                      command=addNewButtonHandler)
addNewButton.pack(side=TOP, pady=(10, 0), padx=(0, 10))

win.mainloop()
