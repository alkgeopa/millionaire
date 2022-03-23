from tkinter import *
from Primitives import *
from pygame import mixer
from PIL import ImageTk, Image


class MainMenuLevel:
    def __init__(self, root: Tk) -> None:
        self.backgroundColor = '#202169'
        self.foregroundColor = 'white'
        self.hoverBackgroundColor = 'white'
        self.hoverForegroundColor = 'black'

        self.mainFrame = Frame(root, background='black', padx=32, pady=16)
        self.mainFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.img = self.initImage()
        self.logo = Label(self.mainFrame, image=self.img, background='black')
        self.logo.pack(side=TOP, anchor=N)

        fontOptions = ('Segoe UI', 30, 'bold')
        self.gameStart = AHoverButton(self.mainFrame, background='#202169', foreground='white',
                                      font=fontOptions, borderwidth=0, width=15, height=1, text='START')
        self.gameStart.pack(side=TOP, anchor=N, pady=5)

        self.hof = AHoverButton(self.mainFrame, background='#202169', foreground='white',
                                font=fontOptions, borderwidth=0, width=15, height=1, text='HALL OF FAME')
        self.hof.pack(side=TOP, anchor=N, pady=5)

        self.exit = AHoverButton(self.mainFrame, background='#202169', foreground='white',
                                 font=fontOptions, borderwidth=0, width=15, height=1, command=root.destroy, text='EXIT')
        self.exit.pack(side=TOP, anchor=N, pady=5)

        mixer.init()
        mixer.music.load('./sound/happy-8bit-pixel-adenture.wav')
        mixer.music.play(loops=-1, fade_ms=5000)
        mixer.music.set_volume(0.05)

    def initImage(self) -> ImageTk.PhotoImage:
        img = Image.open('./img/logo.png')
        img = img.resize((250, 250), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        return img