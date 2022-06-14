from __future__ import annotations

from typing import TypedDict

"""Collection of custom types"""


class Document(TypedDict):
    text: str
    difficulty: str
    correct: str
    wrong: wrongAnswers


class wrongAnswers(TypedDict):
    w1: str
    w2: str
    w3: str


class Player(TypedDict):
    name: str
    amountWon: int
    totalTime: int
    averageQuestionTime: float
    score: float


class AmountType(TypedDict):
    string: str
    numeric: int
