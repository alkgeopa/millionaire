from tkinter import *
from tkinter.ttk import Treeview, Style

from click import style


class TopTenView(Frame):
    def __init__(
        self, master: Misc | None = ..., controller=None, playerList=..., **kw
    ):
        super().__init__(master=master, **kw)
        self.controller = controller
        # self.place(relx=0.5, rely=0, anchor=N)
        self.pack(side=TOP, anchor=N, expand=1, fill=BOTH)
        # # root είναι το self, δηλαδή στα στοιχεία βάζουμε όρισμα master=self
        #
        # # Η λίστα με τα στοιχεία των παικτών είναι στο self.controller.playersInfo
        #   ή κάνουμε επανάληψη με τη χρήση του generator self.controller.getNextPlayer()
        #
        # # Με χρήση label προβάλλουμε τα στοιχεία των παικτών
        #
        # # Καλό θα είναι τα στοιχεία να μπουν σε .grid() ώστε να φαίνονται καλύτερα
        #
        #
        #
        # Από εδώ αρχίζουμε να γράφουμε (άμα θέλουμε σβήνουμε ό,τι υπάρχει)
        self["background"] = "brown"
        self["padx"] = 20
        self["pady"] = 40

        self.title = Label(self, text="TOP 10 PLAYERS", font=("san-serif", 20, "bold"))
        self.title.pack()

        self.list = PlayerList(self, playerList)


class PlayerList(Treeview):
    def __init__(self, master: Misc | None = ..., playersInfo=None, **kw):
        super(PlayerList, self).__init__(master=master, **kw)
        self.playersInfo = playersInfo
        self["columns"] = ("Player", "Amount", "TotalTime", "AverageTime", "Score")
        # self["selectmode"] = "none"
        self.column("#0", width=0, stretch=False)
        self.column("Player", width=150)
        self.column("Amount", width=150)
        self.column("TotalTime", width=150)
        self.column("AverageTime", width=150)
        self.column("Score", width=150)
        self.heading("#0", text="")
        self.heading("Player", text="Player", anchor=W)
        self.heading("Amount", text="Amount Won", anchor=W)
        self.heading("TotalTime", text="Total Time", anchor=W)
        self.heading("AverageTime", text="Average Question Time", anchor=W)
        self.heading("Score", text="Score", anchor=W)
        self.initList(self.playersInfo)

        style = Style()
        style.configure(
            "playerList.Treeview",
            font=("san-serif", 20, "bold"),
        )
        style.configure(
            "playerList.Treeview.Heading",
            font=("san-serif", 12, "bold"),
        )
        style.configure("playerList.Treeview", rowheight=50)
        self["style"] = "playerList.Treeview"
        self.pack(side=TOP, anchor=N, pady=(10, 0), expand=1, fill=X)

    def initList(self, playersInfo):
        for i, player in enumerate(playersInfo):
            self.insert(
                parent="",
                index=i,
                iid=i,
                values=(
                    player["name"],
                    player["amountWon"],
                    player["totalTime"],
                    player["averageQuestionTime"],
                    player["score"],
                ),
            )
