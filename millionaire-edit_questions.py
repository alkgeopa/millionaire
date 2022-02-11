from textwrap import fill
from tkinter import *
from tinydb import *


# GUI stuff

win = Tk()

win.title('Επεξεργασία ερωτήσεων - Ποιός θέλει να γίνει εκατομμυριούχος')

win.geometry('800x600')

# TODO
# Scrollbars
scrollbarVertical = Scrollbar(win)
scrollbarVertical.pack(side=RIGHT, fill=Y)
scrollbarHorizontal = Scrollbar(win, orient=HORIZONTAL)
scrollbarHorizontal.pack(side=BOTTOM, fill=X)


frameLeft = Frame(win, bg='#ccc', width=300, borderwidth=1)
frameLeft.pack(side=LEFT, fill=Y)

frameRight = Frame(win, bg='#aaa', width=500, border=1)
frameRight.pack(side=LEFT, fill=BOTH, expand=1)

win.mainloop()
