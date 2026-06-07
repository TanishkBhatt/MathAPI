from pydantic import BaseModel
from typing import List, Dict

from backend.models.api.questions import (
    Topic,
    Difficulty,
    Question
)

class Step(BaseModel):
    theory: str
    formulae: Dict[str, str] | None
    calculations: List[str] | None

class Example(BaseModel):
    question: str
    difficulty: Difficulty
    solution: List[Step]
    answer: str|int|float|bool|None

class Explain(BaseModel):
    topic: Topic
    definition: str
    origin: str
    applications: str
    formulae: Dict[str, str] | None
    examples: List[Example]
    try_yourself_questions: List[Question]