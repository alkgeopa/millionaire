import random
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


#################################


# ************************
# Scrollable Frame Class
# ************************
class ScrollFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent)  # create a frame (self)

        # place canvas on self
        self.canvas = Canvas(self, borderwidth=0, background="#ffffff")
        # place a frame on the canvas, this frame will hold the child widgets
        self.viewPort = Frame(self.canvas, background="#ffffff")
        # place a scrollbar on self
        self.vsb = Scrollbar(self, orient="vertical",
                             command=self.canvas.yview)
        # attach scrollbar action to scroll of canvas
        self.canvas.configure(yscrollcommand=self.vsb.set)

        # pack scrollbar to right of self
        self.vsb.pack(side="right", fill="y")
        # pack canvas to left of self and expand to fil
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_window = self.canvas.create_window((4, 4), window=self.viewPort, anchor="nw",  # add view port frame to canvas
                                                       tags="self.viewPort")

        # bind an event whenever the size of the viewPort frame changes.
        self.viewPort.bind("<Configure>", self.onFrameConfigure)
        # bind an event whenever the size of the canvas frame changes.
        self.canvas.bind("<Configure>", self.onCanvasConfigure)

        # bind wheel events when the cursor enters the control
        self.viewPort.bind('<Enter>', self.onEnter)
        # unbind wheel events when the cursorl leaves the control
        self.viewPort.bind('<Leave>', self.onLeave)

        # perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize
        self.onFrameConfigure(None)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox(
            "all"))  # whenever the size of the frame changes, alter the scroll region respectively.

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        # whenever the size of the canvas changes alter the window region respectively.
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

    # cross platform scroll wheel event
    def onMouseWheel(self, event):
        if platform.system() == 'Windows':
            self.canvas.yview_scroll(int(-1 * (event.delta/120)), "units")
        elif platform.system() == 'Darwin':
            self.canvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")

    # bind wheel events when the cursor enters the control
    def onEnter(self, event):
        if platform.system() == 'Linux':
            self.canvas.bind_all("<Button-4>", self.onMouseWheel)
            self.canvas.bind_all("<Button-5>", self.onMouseWheel)
        else:
            self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)

    # unbind wheel events when the cursorl leaves the control
    def onLeave(self, event):
        if platform.system() == 'Linux':
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")
        else:
            self.canvas.unbind_all("<MouseWheel>")


# ********************************
# Example usage of the above class
# ********************************

class Example(Frame):
    def __init__(self, root):

        Frame.__init__(self, root)
        self.scrollFrame = ScrollFrame(self)  # add a new scrollable frame.

        # Now add some controls to the scrollframe.
        # NOTE: the child controls are added to the view port (scrollFrame.viewPort, NOT scrollframe itself)
        for row in range(100):
            a = row
            Label(self.scrollFrame.viewPort, text="%s" % row, width=3, borderwidth="1",
                  relief="solid").grid(row=row, column=0)
            t = "this column is the second column for row %s" % row
            Button(self.scrollFrame.viewPort, text=t, command=lambda x=a: self.printMsg(
                "Hello " + str(x))).grid(row=row, column=1)

        # when packing the scrollframe, we pack scrollFrame itself (NOT the viewPort)
        self.scrollFrame.pack(side="top", fill="both", expand=True)

    def printMsg(self, msg):
        print(msg)


Example(labelFrameLeft).pack(side="top", fill="both", expand=True)

###########################


win.mainloop()
