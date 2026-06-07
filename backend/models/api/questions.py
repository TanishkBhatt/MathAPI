from pydantic import BaseModel
from typing import List
from enum import Enum

from backend.models.api.topics import (
    Topic, 
    Difficulty
)

class Options(BaseModel):
    A: str|int|float|bool|None
    B: str|int|float|bool|None
    C: str|int|float|bool|None
    D: str|int|float|bool|None

class Answer(Enum):
    a = "A"
    b = "B"
    c = "C"
    d = "D"

class Question(BaseModel):
    topic: Topic
    question: str
    difficulty: Difficulty
    options: Options
    answer: Answer

class Questions(BaseModel):
    questions: List[Question]