from pydantic import BaseModel
from typing import List, Dict
from enum import Enum

class Branch(Enum):
    arithmetic = "Arithmetic"
    number_theory = "Number Theory"
    algebra = "Algebra"
    geometry = "Geometry"
    mensuration = "Mensuration"
    coordinate_geometry = "Coordinate Geometry"
    trigonmetry = "Trigonmetry"
    combinatorics = "Combinatorics"
    probability = "Probability"
    statistics = "Statistics"
    relations_functions = "Relations and Functions"
    introductory_linear_algebra = "Introductory Linear Algebra"
    introductory_calculas = "Introductory Calculas"

class Difficulty(Enum):
    beginner = "Beginner"
    intermediate = "Intermediate"
    advanced = "Advanced"

class Options(BaseModel):
    A: str
    B: str
    C: str
    D: str

class Answer(Enum):
    a = "A"
    b = "B"
    c = "C"
    d = "D"

class QuestionType(Enum):
    conceptual = "Conceptual"
    numerical = "Numerical"
    to_prove = "To Prove"
    word_problem = "Word Problem"
    case_based = "Case Based"
    hots = "High Order Thinking Skills"

class Example(BaseModel):
    question: str
    difficulty: Difficulty
    options: Options
    key_observation: str
    concept_used: List[str]
    formulae_used: List[Dict[str, str]]
    answer: Answer
    interpretation: str

class Explination(BaseModel):
    title: str
    content: str

class Formula(BaseModel):
    title: str
    plain_text: str
    latex_code: str

class LearningSource(BaseModel):
    title: str
    type: str
    link: str

class SolutionSource(BaseModel):
    source: str
    type: str
    link: str

class SourceImage(BaseModel):
    title: str
    link: str