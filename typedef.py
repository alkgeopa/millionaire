from typing import TypedDict, Callable


# TYPE DEFINITIONS


class wrongAnswers:
    pass


class Document(TypedDict):
    text: str
    difficulty: str
    correct: str
    wrong: wrongAnswers


class wrongAnswers(TypedDict):
    w1: str
    w2: str
    w3: str
