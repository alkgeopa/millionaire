from __future__ import annotations

from typing import TypedDict


# TYPE DEFINITIONS


class Question(TypedDict):
    text: str
    difficulty: str
    correct: str
    wrong: WrongAnswers


class WrongAnswers(TypedDict):
    w1: str
    w2: str
    w3: str


class QuestionModel(TypedDict):
    text: str
    answers: list[str]


class Player(TypedDict):
    name: str
    amountWon: int
    totalTime: float
    averageQuestionTime: float
    score: float
