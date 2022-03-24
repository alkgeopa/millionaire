from tkinter import *
from Primitives import *
from typedef import *
from pygame import mixer
from PIL import ImageTk, Image




class UsernameInput:
    pass


class MainMenuLevel:
    def __init__(self, root: Tk, callback: Callable) -> None:
        self.root = root
        self.callback = callback

        self.mainFrame = Frame(root, background='black', padx=32, pady=16)
        self.mainFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.img = self.initImage()
        self.logo = Label(self.mainFrame, image=self.img, background='black')
        self.logo.pack(side=TOP, anchor=N)

        fontOptions = ('Segoe UI', 30, 'bold')
        # Start button init
        self.gameStart = AHoverButton(self.mainFrame, background='#202169', foreground='white',
                                      font=fontOptions, borderwidth=0, width=15, height=1, command=self.startHandler, text='START')
        self.gameStart.pack(side=TOP, anchor=N, pady=5)

        # Hall of fame button init
        self.hof = AHoverButton(self.mainFrame, background='#202169', foreground='white',
                                font=fontOptions, borderwidth=0, width=15, height=1, text='HALL OF FAME')
        self.hof.pack(side=TOP, anchor=N, pady=5)

        # Exit button init
        self.exit = AHoverButton(self.mainFrame, background='#202169', foreground='white',
                                 font=fontOptions, borderwidth=0, width=15, height=1, command=root.destroy, text='EXIT')
        self.exit.pack(side=TOP, anchor=N, pady=5)

        # Menu music init
        mixer.init()
        mixer.music.load('./sound/happy-8bit-pixel-adenture.wav')
        mixer.music.play(loops=-1, fade_ms=5000)
        mixer.music.set_volume(0.05)

    def initImage(self) -> ImageTk.PhotoImage:
        '''
        Prepares and returns the logo image
        '''
        img = Image.open('./img/logo.png')
        img = img.resize((250, 250), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        return img

    def startHandler(self) -> None:
        '''
        Callback handler function for the Start Button

        Destroys the menu widgets and creates a user input widget
        '''
        for child in self.root.winfo_children():
            child.destroy()

        mixer.music.stop()

        usernameInput = UsernameInput(self.root, self.callback)

    def hofHandler(self) -> None:
        '''
        '''


class UsernameInput:
    def __init__(self, root: Tk, callback: Callable) -> None:
        self.callback = callback

        self.mainFrame = Frame(root, background='black', padx=32, pady=16)
        self.mainFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.textPrompt = Label(
            self.mainFrame, background='black', foreground='white', text='Enter your name')
        self.textPrompt.pack()

        self.username = StringVar()
        self.entry = ATextEntry(
            self.mainFrame, background='white', relief='flat')
        self.entry.pack(side=TOP, anchor=N)

        self.okButton = AHoverButton(
            self.mainFrame, background='#202169', foreground='white', border=0, width=10, command=self.okHandler, text='OK')
        self.okButton.pack(side=TOP, anchor=N, pady=30)

    def okHandler(self) -> None:
        self.callback()
