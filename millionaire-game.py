from tkinter import *

# STATE DEFINITIONS

# currentView
MAINMENU = 'mainmenu'
HALLOFFAME = 'halloffame'
GAME = 'game'

# stage
EASY = 'easy'
MEDIUM = 'medium'
HARD = 'hard'

##-----------------

class Game:
    state = {}

    @staticmethod
    def resetGameState():
        Game.state = {
            'currentView': None,
            'started': NO,
            'stage': None,
            'victory': None,
        }

class Player:
    pass


class MainMenu:
    pass


class HallOfFame:
    pass


class Question:
    pass


class Lifeline:
    pass


class Money:
    pass
