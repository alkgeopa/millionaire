from numpy.random import choice
from tinydb import TinyDB, Query
from random import shuffle
from typedef import *

db = TinyDB("db.json")


def countAllQuestions() -> int:
    question = Query()
    db.table("questions").__sizeof__()
    return db.table("questions").count(question.text > "")


def prepareQuestions(difficulty: str) -> list[Document]:
    if not difficulty.isalpha():
        raise Exception("@ getRandomQuestion(): The difficulty argument is not a letter.")

    question = Query()
    questionList = db.table("questions").search(question.difficulty == difficulty)

    return questionList


def getQuestions():
    """
    Returns a ``dictionary`` with ``3 arrays``, each containing ``6 questions``,
    one extra for each difficulty for the skip lifeline
    """

    easyQuestions = prepareQuestions("ε")
    mediumQuestions = prepareQuestions("μ")
    hardQuestions = prepareQuestions("δ")

    shuffle(easyQuestions)
    easy = 8 * [Document]
    for index in range(8):
        if easyQuestions:
            easy[index] = easyQuestions.pop()
        else:
            break

    shuffle(mediumQuestions)
    medium = 8 * [Document]
    for index in range(8):
        if mediumQuestions:
            medium[index] = mediumQuestions.pop()
        else:
            break

    shuffle(hardQuestions)
    hard = 8 * [Document]
    for index in range(8):
        if hardQuestions:
            hard[index] = hardQuestions.pop()
        else:
            break

    return {"easy": easy, "medium": medium, "hard": hard}




def getRandomQuestion(difficulty: str = None) -> Document:
    """Returns a random question as a ``document``.
    If a ``difficulty`` string  is provided (``'ε'`` or ``'μ'`` or ``'δ'``)
    then the returned question is of the specified difficulty
    """
    question = Query()
    if not difficulty:
        questionList = db.table("questions").all()
        return choice(questionList)
    questionList = db.table("questions").search(question.difficulty == difficulty)
    return choice(questionList)


def seedPlayers() -> None:
    playerTable = db.table("Players")
    if playerTable.all():
        return

    seedData = [
        {
            "name": "john",
            "amountWon": 10000,
            "totalTime": 600,
            "averageQuestionTime": 54.5454,
            "score": 16.67,
        },
        {
            "name": "jim",
            "amountWon": 3500,
            "totalTime": 160,
            "averageQuestionTime": 20,
            "score": 21.88,
        },
        {
            "name": "new_player397",
            "amountWon": 1000,
            "totalTime": 50,
            "averageQuestionTime": 10,
            "score": 20,
        },
    ]
    playerTable.insert_multiple(seedData)


def getAllPlayers() -> list:
    playerTable = db.table("Players")
    return playerTable.all()


def getTopTenPlayers() -> list:
    allPlayers = getAllPlayers()
    topTen = []
    for i in range(10):
        if allPlayers:
            maxPlayer = max(allPlayers, key=lambda p: p['score'])
            topTen.append(maxPlayer)
            allPlayers.remove(maxPlayer)

    return topTen
