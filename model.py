from __future__ import annotations

from numpy.random import shuffle
from tkinter import StringVar
from time import time
from typing import TypedDict


# class AnswerVar(StringVar):
#     def __init__(self, text: str, correct: bool, **kw) -> None:

#         if 'master' in kw:
#             super().__init__(self, master=kw['master'], value=text, **kw)
#         self.correct: bool = correct

#     def __repr__(self) -> str:
#         if self.correct:
#             return f"|>{self.get()}<|"
#         return f"{self.get()}"


# class Model:
#     def __init__(self) -> None:
#         pass


# class Game(Model):
#     def __init__(self) -> None:
#         super().__init__()
#         self.level: int = 0
#         self.stage: int = 0
#         self.lives: int = 3
#         self.playerName: str = ''

#     def __repr__(self) -> str:
#         return f"stage:\t\t{self.stage}\nlevel:\t\t{self.level}\nlives:\t\t{self.lives}"

#     def levelUp(self):
#         self.level += 1
#         self.stage = self.level // 5

#     def livesDown(self):
#         self.lives.set(self.lives.get() - 1)

#     def setPlayerName(self, name: str):
#         self.playerName = name


# class Question(Model):
#     class QuestionModel(TypedDict):
#         text: str
#         answers: list[Answer]

#     def __init__(self, question: QuestionModel) -> None:
#         super().__init__()
#         self.questionText: str = question['text']
#         self.answers: list[Answer] = question['answers']
#         shuffle(self.answers)

#     def __repr__(self) -> str:
#         return f"question:\t{self.questionText}\nanswers:\t{self.answers}"


# class Answer(Model):
#     def __init__(self, text: str, correct: bool) -> None:
#         super().__init__()
#         self.text: str = text
#         self.correct: bool = correct

#     def __repr__(self) -> str:
#         if self.correct:
#             return f"|>{self.text}<|"
#         else:
#             return f"{self.text}"

