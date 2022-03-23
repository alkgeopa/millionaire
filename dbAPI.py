from tinydb import TinyDB, Query
from random import choices
from typedef import *


db = TinyDB('db.json')


def getRandomQuestion(difficulty: str) -> Document:
    '''
    Returns a random ``document`` with a question of difficulty=``difficulty``
    '''
    if not difficulty.isalpha():
        print('@ getRandomQuestion(): The difficulty argument is not a letter.')
        return None

    Question = Query()
    questionList = db.table('questions').search(
        Question.difficulty == difficulty)
    return choices(questionList, k=3)
