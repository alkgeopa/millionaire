from tkinter import *
from Primitives import *
from typedef import *
from pygame import mixer
from PIL import ImageTk, Image


class MainMenu(Frame):
    def __init__(self, master: Misc | None = ..., **kw) -> None:
        super().__init__(master=master, **kw)

        self.root = master
        self.place(relx=0.5, rely=0.5, anchor=CENTER)
        self['background'] = 'black'
        self.img = self.initImage()
        self.logo = Label(self, image=self.img, background='black')
        self.logo.pack(side=TOP, anchor=N)

        fontOptions = ('Segoe UI', 30, 'bold')
        # Start button init
        self.gameStart = AHoverButton(self, background='#202169', foreground='white',
                                      font=fontOptions, borderwidth=0, width=15, height=1, command=self.startHandler, text='START')
        self.gameStart.pack(side=TOP, anchor=N, pady=5)

        # Hall of fame button init
        self.hof = AHoverButton(self, background='#202169', foreground='white',
                                font=fontOptions, borderwidth=0, width=15, height=1, text='HALL OF FAME')
        self.hof.pack(side=TOP, anchor=N, pady=5)

        # Exit button init
        self.exit = AHoverButton(self, background='#202169', foreground='white',
                                 font=fontOptions, borderwidth=0, width=15, height=1, command=self.root.quit, text='EXIT')
        self.exit.pack(side=TOP, anchor=N, pady=5)

        # Menu music init
        mixer.init()
        mixer.music.load('./sound/main-theme.mp3')
        mixer.music.play(loops=-1)
        mixer.music.set_volume(0.3)

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

    def hofHandler(self) -> None:
        '''
        '''
