from time import time
from tkinter import IntVar, StringVar, messagebox, Event

from numpy.random import shuffle, choice

from constants import *
from dbAPI import getQuestions, getTopTenPlayers, savePlayerData
from gameView import GameView
from menuView import MainMenu
from playerNameInputView import PlayerNameInputView
from questionFrame import QuestionFrame
from sidePanelFrame import SidePanelFrame
from topTenView import TopTenView
from resultFrame import DefeatView, SafetyNetView, MillionaireView


class Controller:
    appRoot = None

    def __init__(self) -> None:
        ...


class ApplicationController(Controller):
    def __init__(self, appRoot) -> None:
        super(ApplicationController, self).__init__()
        Controller.appRoot = appRoot
        self.currentController: MainMenuController | GameController | TopTenController = MainMenuController(self)

    def setController(self, controller):
        if self.currentController:
            del self.currentController
        self.currentController = controller()

    def exitToMainMenu(self):
        res = messagebox.askyesno('Επιβεβαίωση εξόδου',
                                  'Θέλετε να σταματήσετε το παιχνίδι;\nΚανένα σκορ δε θα αποθηκευτεί.')
        if res:
            self.setMainMenuController()

    def setMainMenuController(self):
        self.delCurrentView()
        if self.currentController:
            del self.currentController
        self.currentController = MainMenuController(self)

    def delCurrentView(self):
        try:
            self.currentController.currentView.destroy()
        except AttributeError:
            self.currentController.gameView.destroy()


class MainMenuController(Controller):
    def __init__(self, appController) -> None:
        super(MainMenuController, self).__init__()
        self.appController = appController
        self.currentView = MainMenu(self.appRoot, self)

    def startHandler(self):
        self.currentView.destroy()
        self.appController.setController(
            lambda: PlayerNameController(self.appController)
        )

    def topTenHandler(self):
        self.currentView.destroy()
        self.appController.setController(lambda: TopTenController(self.appController))


class PlayerNameController(Controller):
    def __init__(self, appController) -> None:
        super(PlayerNameController, self).__init__()
        self.appController = appController
        self.playerName = StringVar()
        self.currentView = PlayerNameInputView(self.appRoot, controller=self)

    def startHandler(self, event: Event | None = ...):
        print(f"{self.playerName.get() = }")
        self.currentView.destroy()
        self.appController.setController(
            lambda: GameController(self.appController, self.playerName)
        )


class GameController(Controller):
    def __init__(self, appController: ApplicationController, playerName: StringVar = None) -> None:
        super(GameController, self).__init__()
        self.appController = appController
        self.gameView = GameView(self.appRoot)
        self.gameView.backToMenuButton.config(command=self.appController.exitToMainMenu)
        self.playerName = playerName
        self.stage = 0
        self.level = 0
        self.livesVar = IntVar(value=3)
        self.questionTimes: list[int] = []
        self.amountWon: int = 0

        self.questionPool = getQuestions()

        self.questionController = QuestionController(self.gameView, self)
        self.questionController.questionInit()

        self.lifelinesController = LifelineController(self.gameView, self)

        self.sidePanel = SidePanelFrame(self.gameView, self.lifelinesController)

    def getNextQuestion(self):
        if self.stage == 0:
            return self.questionPool["easy"].pop()
        if self.stage == 1:
            return self.questionPool["medium"].pop()
        if self.stage == 2:
            return self.questionPool["hard"].pop()

    def nextQuestion(self, result: str):
        if self.livesVar.get() > 0:
            if result == "correct":
                self.questionTimes.append(60 - self.questionController.timer.get())
                self.level += 1
                if 5 <= self.level < 10:
                    self.stage = 1
                if self.level >= 10:
                    self.stage = 2

                if self.level == 14:
                    self.amountWon = AMOUNTS[14]['numeric']
                    print('YOU ARE A MILLIONAIRE!')
                    self.savePlayer()
                    self.renderResults('millionaire')
                    return

                self.replaceQuestion()

                self.sidePanel.destroy()
                self.sidePanel = SidePanelFrame(self.gameView, self.lifelinesController)
            else:
                self.replaceQuestion()

                self.sidePanel.destroy()
                self.sidePanel = SidePanelFrame(self.gameView, self.lifelinesController)
        else:
            self.checkSafetyNet()

    def replaceQuestion(self):
        self.questionController.questionFrame.destroy()
        self.questionController = QuestionController(self.gameView, self)
        self.questionController.questionInit()

    def updateLives(self):
        self.livesVar.set(self.livesVar.get() - 1)

    def checkSafetyNet(self):
        if self.stage == 1:
            self.amountWon = AMOUNTS[4]['numeric']
            print(f'Κέρδισες το 1ο μαξιλαράκι: {self.amountWon}')
            self.savePlayer()
            self.renderResults('safetynet')
        elif self.stage == 2:
            self.amountWon = AMOUNTS[9]['numeric']
            print(f'Κέρδισες το 2ο μαξιλαράκι: {self.amountWon}')
            self.savePlayer()
            self.renderResults('safetynet')
        else:
            print('Έχασες!')
            self.renderResults('defeat')

    def renderResults(self, res: str):
        if res == 'defeat':
            self.questionController.questionFrame.destroy()
            DefeatView(self.gameView, self)
        elif res == 'safetynet':
            self.questionController.questionFrame.destroy()
            SafetyNetView(self.gameView, self)
        else:
            self.questionController.questionFrame.destroy()
            MillionaireView(self.gameView, self)

    def savePlayer(self):
        if not self.playerName:
            self.playerName = 'New Player'
        totalTime = sum(self.questionTimes)
        averageTime = round(totalTime / len(self.questionTimes), 2)
        score = round(self.amountWon / totalTime, 2)
        playerInfo = {
            "name": self.playerName.get(),
            "amountWon": self.amountWon,
            "totalTime": totalTime,
            "averageQuestionTime": averageTime,
            "score": score
        }
        savePlayerData(playerInfo)

    def delTwoWrongAnswers(self):
        wrong = list(self.questionController.wrongAnswers.values())
        shuffle(wrong)

        for answerButton in self.questionController.questionFrame.answer:
            if answerButton.text in wrong[:-1]:
                answerButton.grid_forget()

    def computer(self):
        weights: list[float] = []

        isHidden = False
        for answerButton in self.questionController.questionFrame.answer:
            if not answerButton.winfo_viewable():
                isHidden = True
                break

        if isHidden:
            for answerButton in self.questionController.questionFrame.answer:
                print(answerButton.text)
                if answerButton.text == self.questionController.correctAnswer:
                    weights.append(0.4)
                else:
                    if not answerButton.winfo_viewable():
                        weights.append(0)
                    else:
                        weights.append(0.6)
        else:
            for answerButton in self.questionController.questionFrame.answer:
                if answerButton.text == self.questionController.correctAnswer:
                    weights.append(0.4)
                else:
                    weights.append(0.2)

        suggestion = choice(self.questionController.questionFrame.answer, p=weights)
        suggestion.changeToSuggestion()


class QuestionController(Controller):
    def __init__(self, root, gameController) -> None:
        super(QuestionController, self).__init__()
        self.gameController = gameController
        self.playerName = self.gameController.playerName
        questionInfo = self.gameController.getNextQuestion()
        self.questionText = questionInfo["text"]
        self.correctAnswer = questionInfo["correct"]
        self.wrongAnswers = questionInfo["wrong"]
        self.shuffledAnswers = []
        self.shuffledAnswers.append(self.correctAnswer)
        for answer in self.wrongAnswers.values():
            self.shuffledAnswers.append(answer)
        shuffle(self.shuffledAnswers)

        self.gameRoot = root
        self.questionFrame = None

        self.timeStart = time()
        self.timer = IntVar(value=60)
        self.timerAfter = None

        print('-' * 10)
        print(f'stage:\t\t{self.gameController.stage}')
        print(f'level:\t\t{self.gameController.level}')
        print(f'amount:\t\t{AMOUNTS[self.gameController.level]["string"]}')
        print(f'lives:\t\t{self.gameController.livesVar.get()}')
        print(f'questionText:\t{self.questionText}')
        print(f'correctAnswer:\t{self.correctAnswer}')
        print(f'shuffledAnswers:{self.shuffledAnswers}')

    def questionInit(self):
        if self.timerAfter:
            self.gameRoot.after_cancel(self.timerAfter)
        self.questionFrame = QuestionFrame(master=self.gameRoot, controller=self)

    def checkAnswer(self, event):
        print(f"selectedAnswer: {event.widget.text}")

        if self.timerAfter:
            self.gameRoot.after_cancel(self.timerAfter)

        button = event.widget
        button.changeToOrange()

        if event.widget.text == self.correctAnswer:
            print("Selected the CORRECT answer")

            button.after(4000, button.changeToGreen)

            if self.gameController.level < 14:
                button.after(8000, self.gameController.nextQuestion, "correct")
            else:
                print("Κέρδισες!")  # TODO
        else:
            print("Selected the WRONG answer")

            button.after(4000, button.changeToRed)
            button.after(4000, self.gameController.updateLives)

            for i in range(4):
                correctbutton = self.questionFrame.answer[i]
                if self.questionFrame.answer[i].text == self.correctAnswer:
                    correctbutton.after(4000, correctbutton.changeToGreen)

            for i in range(4):
                self.questionFrame.answer[i].changeState()

            button.after(8000, self.gameController.nextQuestion, "wrong")

    def updateTimer(self):
        if self.timer.get() > 0:
            # όσο έχουμε ζωές...
            self.timer.set(self.timer.get() - 1)
        else:
            # έληξε ο χρόνος οπότε χάσε μια ζωή και πήγαινε στην επόμενη
            self.gameController.updateLives()
            self.questionFrame.timer.config(bg='red')
            self.gameRoot.after(2000, self.gameController.nextQuestion, "wrong")
            return
        # αναδρομική κλήση σε 1000ms
        self.timerAfter = self.gameRoot.after(1000, self.updateTimer)

    # generator
    def getNextAnswer(self) -> str:
        for answer in self.shuffledAnswers:
            yield answer


class LifelineController(Controller):
    def __init__(self, gameView, gameController) -> None:
        super(LifelineController, self).__init__()
        self.gameController = gameController
        self.list = ['50-50', 'skip', 'computer']

    def lifelineHandler(self, event):
        print(f'lifeline:\t{event.widget.text}')
        event.widget.destroy()

        if event.widget.text == "skip":
            self.list.remove("skip")
            self.gameController.replaceQuestion()
        elif event.widget.text == "50-50":
            self.list.remove("50-50")
            self.gameController.delTwoWrongAnswers()
        else:
            self.gameController.computer()
            self.list.remove("computer")


class TopTenController(Controller):
    def __init__(self, appController: ApplicationController) -> None:
        super(TopTenController, self).__init__()
        self.appController = appController
        self.playersInfo = getTopTenPlayers()
        self.currentView = TopTenView(self.appRoot, self)

    # generator
    def getNextPlayer(self) -> None:
        for player in self.playersInfo:
            yield player

    def mainMenuView(self):
        self.currentView.destroy()
        self.appController.setController(lambda: MainMenuController(self.appController))
