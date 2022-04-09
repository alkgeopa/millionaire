# example 1
# tkinter simple gui

from tkinter import *


class MainWindow:
    def __init__(self) -> None:
        # Create window (root widget)
        self.win = Tk()

        # Initial size in pixels (width x height)
        self.win.geometry('800x600')

        # Set the window title
        self.win.title('Test window')

        # Minimum size the window can have
        self.win.minsize(width=400, height=300)

        # Create a frame...
        self.myFrame = Frame(master=self.win, background='yellow', border=4)
        # ...and put it on screen !important!
        self.myFrame.pack(side='top', anchor='n')

        # Create a label (a simple text)...
        self.myTitle = Label(master=self.win, text='This is the title', font=('sans-serif', 20, 'bold'))
        # ...and put it on screen!
        self.myTitle.pack(side='top', anchor='n')

        # Create a + button...
        self.myUpButton = Button(master=self.win, text='Count up', command=self.countUp)
        # ...and put it on screen!
        self.myUpButton.pack(side='top', anchor='n')

        # Variable that holds the counter number
        self.counter = 0
        # Create a label for the counter...
        self.myCounterLabel = Label(master=self.win, text=f'counter: {self.counter}', background='black', foreground='white')
        # ...and put it on screen!
        self.myCounterLabel.pack(side='top', anchor='n', pady=10)

        # Create a - button...
        self.myDownButton = Button(master=self.win, text='Count down', command=self.countDown)
        # ...and put it on screen!
        self.myDownButton.pack(side='top', anchor='n')

    # Callback function for the + button
    def countUp(self) -> None:
        # Increase self.count by 1
        self.counter += 1
        # Update the label text
        self.myCounterLabel['text'] = f'counter: {self.counter}'

    # Callback function for the - button
    def countDown(self) -> None:
        # Decrease self.count by 1
        self.counter -= 1
        # Update the label text
        self.myCounterLabel['text'] = f'counter: {self.counter}'


# Create a MainWindow object
mainWindow = MainWindow()

# Call the tkinter main loop
mainWindow.win.mainloop()

# Any code after the main loop won't execute while the window is running





# But once it closes...
print('\n🎶🎶🎷Never🎵gonna🎵give🎵you🎵up🎷🎶🎶\n')