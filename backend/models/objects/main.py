from pydantic import BaseModel
from typing import List, Dict
from backend.models.objects.helpers import *

class Topic(BaseModel):
    _id: str
    name: str
    branch: Branch
    difficulty: Difficulty
    questions_available: int
    learning_sources_available: int

class Question(BaseModel):
    question: str
    topic: Topic
    difficulty: Difficulty
    question_type: QuestionType
    options: Options
    challange: str
    answer: Answer
    solution_source: str|None

class Explain(BaseModel):
    topic: Topic
    definition: str
    origin: str
    applications: List[str]
    explination: Dict[str, str]
    formulae: Dict[str, str]
    examples: List[Example]
    try_yourself_questions: List[Question]