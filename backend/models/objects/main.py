from pydantic import BaseModel
from typing import List
from backend.models.objects.helpers import *

class Topic(BaseModel):
    topic_id: str
    topic_name: str
    branch: List[Branch]
    difficulty: Difficulty
    prerequisites: List[str]
    related_topics: List[str]
    questions_available: int
    learning_sources_available: int

class Question(BaseModel):
    topic_id: str
    question: str
    difficulty: Difficulty
    question_type: List[QuestionType]
    options: Options
    hint: str|None
    answer: Answer
    solution_sources: List[SolutionSource]

class Explain(BaseModel):
    topic_name: str
    definition: str
    origin: str
    applications: List[str]
    explination: List[Explination]
    formulae: List[Formula]
    examples: List[Example]
    try_yourself_questions: List[Question]
    learning_sources: List[LearningSource]
    source_images: List[SourceImage]