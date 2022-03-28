from tinydb import TinyDB, Query
from random import shuffle
from typedef import *


db = TinyDB('db.json')


def countAllQuestions() -> int:
    Question = Query()
    db.table('questions').__sizeof__()
    return db.table('questions').count(Question.text > '')


def prepareQuestions(difficulty: str) -> list[Document]:
    '''
    Returns ``n`` random ``documents`` with a question of difficulty=``difficulty``
    '''
    if not difficulty.isalpha():
        print('@ getRandomQuestion(): The difficulty argument is not a letter.')
        return None

    Question = Query()
    questionList = db.table('questions').search(
        Question.difficulty == difficulty)

    return questionList


def getQuestions():
    '''
    Returns a ``dictionary`` with ``3 arrays``, each containing ``6 questions``,
    one extra for each difficulty for the swap lifeline
    '''

    easyQuestions = prepareQuestions('ε')
    mediumQuestions = prepareQuestions('μ')
    hardQuestions = prepareQuestions('δ')

    shuffle(easyQuestions)
    easy = 6*[Document]
    for index in range(6):
        if easyQuestions:
            easy[index] = easyQuestions.pop()
        else:
            break

    shuffle(mediumQuestions)
    medium = 6*[Document]
    for index in range(6):
        if mediumQuestions:
            medium[index] = mediumQuestions.pop()
        else:
            break

    shuffle(hardQuestions)
    hard = 6*[Document]
    for index in range(6):
        if hardQuestions:
            hard[index] = hardQuestions.pop()
        else:
            break

    return {
        'easy': easy,
        'medium': medium,
        'hard': hard
    }

