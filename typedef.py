from __future__ import annotations

from typing import TypedDict


# TYPE DEFINITIONS


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
    totalTime: float
    averageQuestionTime: float
    score: float
