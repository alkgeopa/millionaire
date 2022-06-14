from numpy.random import choice, shuffle
from tinydb import TinyDB, Query

from filePath import resourcePath
from typedef import *

db = TinyDB(resourcePath("db.json"))


def countAllQuestions() -> int:
    """
    Count the number of questions on the database
    :return: number of questions
    """

    question = Query()
    return db.table("questions").count(question.text > "")


def prepareQuestions(difficulty: str) -> list[Document]:
    """
    Queries the database for a list of questions of a specific difficulty
    :param difficulty: string that specifies the difficulty
    :return: list of questions as a list of Documents
    """

    if not difficulty.isalpha():
        raise Exception("@ getRandomQuestion(): The difficulty argument is not a letter.")

    question = Query()
    questionList = db.table("questions").search(question.difficulty == difficulty)

    return questionList


def getQuestions() -> dict:
    """
    Returns a ``dictionary`` with ``3 arrays``, each containing ``8 questions``,
    one extra for each difficulty for the skip lifeline and 2 for the spare lives
    """

    easyQuestions = prepareQuestions("ε")
    mediumQuestions = prepareQuestions("μ")
    hardQuestions = prepareQuestions("δ")

    STAGEQUESTIONS = 8
    shuffle(easyQuestions)
    easy = STAGEQUESTIONS * [Document]
    for index in range(STAGEQUESTIONS):
        if easyQuestions:
            easy[index] = easyQuestions.pop()
        else:
            break

    shuffle(mediumQuestions)
    medium = STAGEQUESTIONS * [Document]
    for index in range(STAGEQUESTIONS):
        if mediumQuestions:
            medium[index] = mediumQuestions.pop()
        else:
            break

    shuffle(hardQuestions)
    hard = STAGEQUESTIONS * [Document]
    for index in range(STAGEQUESTIONS):
        if hardQuestions:
            hard[index] = hardQuestions.pop()
        else:
            break

    return {"easy": easy, "medium": medium, "hard": hard}


def getRandomQuestion(difficulty: str = '') -> Document:
    """
    Returns a random question as a ``document``.
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
    """
    Populates the database with some dummy player data
    """

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


def savePlayerData(playerInfo: dict) -> None:
    """
    Saves the stats of the current player
    """

    playerData = {
        "name": playerInfo["name"],
        "amountWon": int(playerInfo["amountWon"]),
        "totalTime": int(playerInfo["totalTime"]),
        "averageQuestionTime": float(playerInfo["averageQuestionTime"]),
        "score": float(playerInfo["score"]),
    }
    print(playerData)
    playerTable = db.table("Players")
    playerTable.insert(playerData)


def getAllPlayers() -> list[Player]:
    """
    Queries the database for the ``Players`` table
    :return: list of all the player documents
    """

    playerTable = db.table("Players")
    return playerTable.all()


def getTopTenPlayers() -> list[Player]:
    """
    Gets the top ten players, in terms of score
    :return: list of the top ten players
    """
    
    allPlayers = getAllPlayers()
    topTen: list[Player] = []
    for i in range(10):
        if allPlayers:
            maxPlayer = max(allPlayers, key=lambda p: p['score'])
            topTen.append(maxPlayer)
            allPlayers.remove(maxPlayer)

    [print(player) for player in topTen]
    print('-' * 100)

    return topTen
