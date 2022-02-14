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


class ScrollFrame(Frame):
    def __init__(self, parent):
        # create a frame
        super().__init__(parent)

        # place a canvas on self
        self.canvas = Canvas(self, borderwidth=0, background=defColor)
        # place a frame in the canvas
        # all child widgets will go inside this frame
        self.viewport = Frame(self.canvas, background=defColor)
        # place scrollbar on self
        self.verticalSrollbar = Scrollbar(self, orient=VERTICAL)
        # attach scrollbar action to the scrolling of the canvas
        self.canvas.configure(yscrollcommand=self.verticalSrollbar.set)

        # pack scrollbar to the right side of self
        self.verticalSrollbar.pack(side=RIGHT, fill=Y)
        # pack canvas to the left side of self
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        # add the viewport frame inside the canvas
        self.canvasWindow = self.canvas.create_window(
            (4, 4), window=self.viewport, anchor=NW, tags="self.viewport")


        # scroll the canvas when dragging the scrollbar with the mouse
        self.verticalSrollbar.config(command=self.canvas.yview)

        # bind an event whenever the size  of the viewport frame changes
        self.viewport.bind('<Configure>', self.onFrameConfigure)
        # bind an event whenever the size of the canvas frame changes
        self.canvas.bind('<Configure>', self.onCanvasConfigure)

        # bind wheel events when the cursor enters (hover) the viewport
        self.viewport.bind('<Enter>', self.onEnter)
        # unbind wheel events when the cursor leaves (unhover) the viewport
        self.viewport.bind('<Leave>', self.onLeave)

        self.onFrameConfigure(None)

    def onFrameConfigure(self, event):
        '''
        Reset the scroll region to fit the inner frame
        '''
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def onCanvasConfigure(self, event):
        '''
        Reset the canvas window to fit the inner frame
        '''
        canvasWidth = event.width
        # when the canvas changes size, change the size of the inner window respectively
        self.canvas.itemconfigure(self.canvasWindow, width=canvasWidth)

    # manage scroll wheel events
    def onMouseWheel(self, event):
        if platform.system() == 'Windows':
            self.canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
        elif platform.system() == 'Darwin':
            self.canvas.yview_scroll(int(-1*event.delta), 'units')
        else:
            if event.num == 4:
                self.canvas.yview_scroll(-1, 'units')
            elif event.num == 5:
                self.canvas.yview_scroll(1, 'units')

    # bind wheel when mouse enters (hover) the canvas

    def onEnter(self, event):
        if platform.system() == 'Linux':
            self.canvas.bind_all('<Button-4>', self.onMouseWheel)
            self.canvas.bind_all('<Button-5>', self.onMouseWheel)
        else:
            self.canvas.bind_all('<MouseWheel>', self.onMouseWheel)

    # unbind wheel when mouse leaves (unhover) the canvas
    def onLeave(self, event):
        if platform.system() == 'Linux':
            self.canvas.unbind_all('<Button-4')
            self.canvas.unbind_all('<Button-5')
        else:
            self.canvas.unbind_all('MouseWheel')


class AScrollableList(Frame):
    def __init__(self, root):

        Frame.__init__(self, root)
        self.scrollFrame = ScrollFrame(self)

        for row in range(100):
            a = row
            # Label(self.scrollFrame.viewport, text="%s" % row, width=3, borderwidth="1",
            #       relief="solid").grid(row=row, column=0)
            # t = "this column is the second column for row %s" % row
            # Button(self.scrollFrame.viewport, text=t, command=lambda x=a: self.printMsg(
            #     "Hello " + str(x)), borderwidth=0).grid(row=row, column=1)
            listItem = Frame(self.scrollFrame.viewport)
            listItem.pack(side=TOP, fill=X, expand=TRUE)
            difficultyLabel = Label(listItem, text=choice(['Ε','Μ','Δ']), width=3, borderwidth=1)
            difficultyLabel.grid(row=0, column=0)
            difficultyLabel.propagate(False)
            t = "this column is the second column for row %s" % row
            questionText = Label(listItem, text=t, borderwidth=0)
            questionText.grid(row=0, column=1)

        self.scrollFrame.pack(side=TOP, fill=BOTH, expand=TRUE)

    def printMsg(self, msg):
        print(msg)


AScrollableList(labelFrameLeft).pack(side=TOP, fill=BOTH, expand=TRUE)

win.mainloop()
