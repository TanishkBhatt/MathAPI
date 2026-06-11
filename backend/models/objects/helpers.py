from pydantic import BaseModel
from typing import List
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

class Example(BaseModel):
    question: str
    difficulty: Difficulty
    key_observation: str
    concept_used: str
    formulae_used: List[str]
    answer: str|int|float|bool|None
    interpretation: str

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

class QuestionType(Enum):
    theoretical = "Theoretical"
    numerical = "Numerical"
    to_prove = "To Prove"
    word_problem = "Word Problem"
    case_based = "Case Based"
    hots = "High Order Thinking Skills"