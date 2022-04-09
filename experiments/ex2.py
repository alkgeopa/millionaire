# tkinter example 2: tkinter control variables
from tkinter import *

# MainWindow inherits the Tk class
# a.k.a. acts like it plus has some extra functionality
class MainWindow(Tk):
    def __init__(self) -> None:
        # Call the parent constructor
        super().__init__()

        # Set the window title
        self.title('Test window')

        # Create a frame...
        self.myFrame = Frame(master=self, background='yellow', border=4)
        # ...and put it on screen !important!
        self.myFrame.pack(side='top', anchor='n')

        # Create a label (a simple text)...
        self.myTitle = Label(master=self, text='This is the title', font=('sans-serif', 20, 'bold'))
        # ...and put it on screen!
        self.myTitle.pack(side='top', anchor='n')

        # Create a + button...
        self.myUpButton = Button(
            master=self, text='Count up', command=self.countUp)
        # ...and put it on screen!
        self.myUpButton.pack(side='top', anchor='n')

        # Create a counterFrame...
        self.counter = counterFrame(self)
        # ...and put it on screen!
        self.counter.pack(side='top', anchor='n', pady=10)

        # Create a - button...
        self.myDownButton = Button(master=self, text='Count down', command=self.countDown)
        # ...and put it on screen!
        self.myDownButton.pack(side='top', anchor='n')

    # Callback function for the + button
    def countUp(self) -> None:
        self.counter.increase()

    # Callback function for the - button
    def countDown(self) -> None:
        self.counter.decrease()

# MainWindow inherits the Frame class
# a.k.a. acts like a Frame plus has some extra functionality/components
class counterFrame(Frame):
    def __init__(self, master: Misc | None = ..., **kw) -> None:
        # Call the parent constructor
        super().__init__(master, **kw)

        # Create a StringVar for the text Label
        self.textVar = StringVar(self, value='counter: ')
        # Create a Label and assign the above stringVar as a textvariable...
        self.textLabel = Label(master=self, textvariable=self.textVar, background='black', foreground='white')
        # ...and put it on screen! (left side)
        self.textLabel.grid(column=0, row=0)

        # Create a IntVar for the number Label
        self.numberVar = IntVar(self, value=0)
        # Create a Label and assign the above IntVar as a textvariable...
        self.numberLabel = Label(master=self, textvariable=self.numberVar, background='black', foreground='white', width=5, anchor='w')
        # ...and put it on screen! (right side)
        self.numberLabel.grid(column=1, row=0)

    def increase(self) -> None:
        # Increase the counter value
        self.numberVar.set(self.numberVar.get() + 1)
        # Set the appropriate color
        self.setColor(self.numberVar.get())

    def decrease(self) -> None:
        # Decrease the counter value
        self.numberVar.set(self.numberVar.get() - 1)
        # Set the appropriate color
        self.setColor(self.numberVar.get())

    def reset(self) -> None:
        # Reset the counter value
        self.numberVar.set(0)
        # Set the appropriate color
        self.setColor(self.numberVar.get())

    def setColor(self, value) -> None:
        if value > 0:
            self.numberLabel['bg'] = 'green'
        elif value == 0:
            self.numberLabel['bg'] = 'black'
        else:
            self.numberLabel['bg'] = 'red'

# Create a MainWindow object
mainWindow = MainWindow()

# Call the tkinter main loop
mainWindow.mainloop()