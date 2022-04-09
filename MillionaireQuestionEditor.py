from tkinter import *
from tkinter.ttk import Treeview
from turtle import width
from tinydb import TinyDB, Query
from typing import TypeVar

# Type definitions
Document = TypeVar('Document')


db = TinyDB('db.json')
# db.drop_tables()    # TODO DELETE
users = db.table('users')
questions = db.table('questions')
dbQuery = Query()

# TODO DELETE


# def dummyData():
#     return [
#         {
#             'text': 'Ποιο είναι το υψηλότερο βουνό της Ελλάδας;',
#             'difficulty': 'ε',
#             'correct': 'Όλυμπος',
#             'wrong': {
#                 'w1': 'Ψηλορείτης',
#                 'w2': 'Σμόλικας',
#                 'w3': 'Παρνασσός',
#             }
#         },
#         {
#             'text': 'Ποιο είναι το ύψος της κορυφής των Ιμαλαΐων, Έβερεστ;',
#             'difficulty': 'μ',
#             'correct': '8.849 μ.',
#             'wrong': {
#                 'w1': '10.534 μ.',
#                 'w2': '5.948 μ.',
#                 'w3': '7.917 μ.',
#             }
#         },
#         {
#             'text': 'Ποιο είναι το βάθος της Τάφρου των Μαριανών;',
#             'difficulty': 'δ',
#             'correct': '10.994 μ.',
#             'wrong': {
#                 'w1': '11.275 μ.',
#                 'w2': '10.534 μ.',
#                 'w3': '11.103 μ.',
#             }
#         },
#         {
#             'text': 'Ποιο από τα παρακάτω δεν είναι έργο του Ουίλλιαμ Σαίξπηρ;',
#             'difficulty': 'μ',
#             'correct': 'Ντάρρεν',
#             'wrong': {
#                 'w1': 'Ο Έμπορος της Βενετίας',
#                 'w2': 'Πολύ κακό για το τίποτα',
#                 'w3': 'Οθέλλος',
#             }
#         }
#     ]


# questions.insert_multiple(dummyData())  # TODO DELETE
allQuestions = questions.all()


# class Question:
#     def __init__(self, text: str, difficulty: int, correct: str, wrong1: str, wrong2: str, wrong3: str):
#         self.text = text


# GUI stuff
win = Tk()

win.title('Επεξεργασία ερωτήσεων - ΠΟΙΟΣ ΘΕΛΕΙ ΝΑ ΓΙΝΕΙ ΕΚΑΤΟΜΜΥΡΙΟΥΧΟΣ')
win.iconbitmap('./img/icon.ico')

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


def openQuestionHandler(options: dict):
    if not OptionFrame.state['open']:
        OptionFrame(options=options)
        OptionFrame.state['open'] = True
    else:
        for widget in labelFrameRight.pack_slaves():
            widget.destroy()
        OptionFrame(options=options)
        OptionFrame.state['open'] = True


class Table:
    global questions

    def __init__(self, parent):
        self.tree = Treeview(parent)
        self.tree['columns'] = ('id', 'difficulty', 'text')
        self.tree.column('#0', width=0, stretch=NO)
        self.tree.column('id', minwidth=80, width=80, stretch=YES)
        self.tree.column('difficulty', anchor=NW,
                         minwidth=50, width=50, stretch=YES)
        self.tree.column('text', anchor=NW)
        self.tree.heading('#0', text='', anchor=W)
        self.tree.heading('id', text=' ID', anchor=W)
        self.tree.heading('difficulty', text=' Δυσκ.', anchor=W)
        self.tree.heading('text', text=' Ερώτηση', anchor=W)

        self.tree.pack(side=BOTTOM, fill=BOTH, expand=YES, pady=(8, 16))

        self.tree.bind('<Button-1>', self.onClick)

    def initInsert(self, allQuestions: list[Document]):
        for i, question in enumerate(allQuestions):
            self.tree.insert(parent='', index=int(question.doc_id), iid=int(question.doc_id), values=(
                str(question.doc_id), question.get('difficulty'), question.get('text'))
            )

    def onClick(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            docId = self.tree.item(item)['values'][0]
            OptionFrame.state['currentDocId'] = docId
            OptionFrame.state['newEntry'] = False
            question = questions.get(doc_id=docId)
            openQuestionHandler({
                'text': question['text'],
                'difficulty': question['difficulty'],
                'correct': question['correct'],
                'wrong': {
                    'w1': question['wrong']['w1'],
                    'w2': question['wrong']['w2'],
                    'w3': question['wrong']['w3'],
                },
            })

    def updateTree(self, allQuestions: list[Document]):
        for question in allQuestions:
            self.tree.insert(parent='', index=int(question.doc_id), iid=int(question.doc_id), values=(
                str(question.doc_id), question.get('difficulty'), question.get('text'))
            )


questionTree = Table(frameLeft)
questionTree.initInsert(questions.all())


class AnswerFrame:
    def __init__(self, parent, text: str = '', textBox: str = '', padx: int = 0, anchor='', width=None):
        self.frame = Frame(parent, pady=10, bg=defColor)
        self.frame.pack(side=TOP, anchor=NW, fill=X)

        self.label = Label(self.frame, text=text, anchor=anchor, padx=padx, width=width, bg=defColor)
        self.label.grid(row=0, column=0)

        self.text = Text(self.frame, font=('Segoe UI', 9), height=1, width=30)
        self.text.grid(row=0, column=1)
        self.text.insert(END, textBox)

    def get(self, index1, index2):
        return self.text.get(index1, index2)


class OptionFrame:

    state = {
        'open': False,
        'duplicate': False,
        'success': False,
        'newEntry': False,
        'currentDocId': None,
    }

    def __init__(self, options=dict()):

        if not options:
            options = {
                'text': '',
                'difficulty': '',
                'correct': '',
                'wrong': {
                    'w1': '',
                    'w2': '',
                    'w3': '',
                },
            }

        self.frame = Frame(labelFrameRight, bg=defColor)
        self.frame.pack(side=TOP, fill=BOTH, expand=YES)

        self.panelText = LabelFrame(
            self.frame, height=100, bg=defColor, text='Κείμενο', padx=5, pady=5)
        self.panelText.pack(side=TOP, anchor=NW, fill=X)

        self.questionText = Text(
            self.panelText, font=('Segoe UI', 9), wrap=WORD, height=4)
        self.questionText.insert(END, options['text'])
        self.questionText.pack(side=TOP, anchor=NW, fill=X)

        self.difficultyFrame = LabelFrame(
            self.frame, bg=defColor, text='Δυσκολία')
        self.difficultyFrame.pack(side=TOP, anchor=NW, fill=X)

        self.difVar = StringVar(None, name='dif')

        if options['difficulty']:
            self.difVar.set(options['difficulty'])

        self.difficultySelelctions = [
            Radiobutton(self.difficultyFrame, text='Εύκολη',
                        justify=LEFT, value='ε', variable='dif', bg=defColor),
            Radiobutton(self.difficultyFrame, text='Μέτρια',
                        justify=LEFT, value='μ', variable='dif', bg=defColor),
            Radiobutton(self.difficultyFrame, text='Δύσκολη',
                        justify=LEFT, value='δ', variable='dif', bg=defColor)
        ]

        if OptionFrame.state['newEntry']:
            self.difVar.set('ε')

        for selection in self.difficultySelelctions:
            selection.pack(side=LEFT, anchor=NW)

        self.answerFrame = LabelFrame(
            self.frame, text='Απαντήσεις', bg=defColor)
        self.answerFrame.pack(side=TOP, anchor=NW, fill=X)

        self.correct = AnswerFrame(
            parent=self.answerFrame, text='Σωστή', anchor='w', textBox=options['correct'], width=10)
        self.wrong1 = AnswerFrame(
            parent=self.answerFrame, text='Λάθος 1', anchor='w', textBox=options['wrong']['w1'], width=10)
        self.wrong2 = AnswerFrame(
            parent=self.answerFrame, text='Λάθος 2', anchor='w', textBox=options['wrong']['w2'], width=10)
        self.wrong3 = AnswerFrame(
            parent=self.answerFrame, text='Λάθος 3', anchor='w', textBox=options['wrong']['w3'], width=10)

        self.buttonGroup = Frame(self.frame, bg=defColor, pady=16)
        self.buttonGroup.pack(side=TOP, anchor=NW)

        self.saveBtn = Button(self.buttonGroup, text='Αποθήκευση' if OptionFrame.state['newEntry'] == True else 'Ενημέρωση',
                              command=lambda: saveButtonHandler(self.getCurrentData()))
        self.saveBtn.grid(row=0, column=0, padx=(0, 10))

        self.cancelBtn = Button(
            self.buttonGroup, text='Άκυρο', command=cancelButtonHandler)
        self.cancelBtn.grid(row=0, column=1, padx=(0, 10))

        self.deleteBtn = Button(self.buttonGroup, text='Διαγραφή',
                                bg='#eaa', command=deleteButtonHandler)
        self.deleteBtn.grid(row=0, column=2, padx=(0, 10))

        OptionFrame.state['currentFrame'] = self.frame

    def getCurrentData(self):
        return {
            'text': self.questionText.get('1.0', END).strip(),
            'difficulty': self.difVar.get(),
            'correct': self.correct.get('1.0', END).strip(),
            'wrong': {
                'w1': self.wrong1.get('1.0', END).strip(),
                'w2': self.wrong2.get('1.0', END).strip(),
                'w3': self.wrong3.get('1.0', END).strip(),
            }
        }


def addNewButtonHandler():
    OptionFrame.state['newEntry'] = True
    if not OptionFrame.state['open']:
        OptionFrame()
        OptionFrame.state['open'] = True
    else:
        OptionFrame.state['open'] = False
        OptionFrame.state['currentDocId'] = None
        for widget in labelFrameRight.pack_slaves():
            widget.destroy()


def saveButtonHandler(doc):
    global questions

    if OptionFrame.state['newEntry']:
        questions.insert(doc)
    else:
        questions.update(doc, doc_ids=[OptionFrame.state['currentDocId']])

    for widget in frameLeft.pack_slaves():
        widget.destroy()

    questionTree = Table(frameLeft)
    questionTree.initInsert(questions.all())

    addNewButton = Button(frameLeft, text='Νέα ερώτηση',
                          command=addNewButtonHandler)
    addNewButton.pack(side=TOP, pady=(10, 0), padx=(0, 10))


def cancelButtonHandler():
    OptionFrame.state['open'] = False
    OptionFrame.state['currentDocId'] = None
    for widget in labelFrameRight.pack_slaves():
        widget.destroy()


def deleteButtonHandler():
    global questionTree, questions

    questions.remove(doc_ids=[OptionFrame.state['currentDocId']])
    cancelButtonHandler()

    for widget in frameLeft.pack_slaves():
        widget.destroy()

    questionTree = Table(frameLeft)
    questionTree.initInsert(questions.all())

    addNewButton = Button(frameLeft, text='Νέα ερώτηση',
                          command=addNewButtonHandler)
    addNewButton.pack(side=TOP, pady=(10, 0), padx=(0, 10))


addNewButton = Button(frameLeft, text='Νέα ερώτηση',
                      command=addNewButtonHandler)
addNewButton.pack(side=TOP, pady=(10, 0), padx=(0, 10))

win.mainloop()
