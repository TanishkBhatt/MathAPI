from pydantic import BaseModel
from enum import Enum

class Branch(Enum):
    arithmetic = "Arithmetic"
    number_theory = "Number Theory"
    algebra = "Algebra"
    geometry = "Geometry"
    coordinate_geometry = "Coordinate Geometry"
    trigonometry = "Trigonometry"
    combinatorics = "Combinatorics"
    probability = "Probability"
    statistics = "Statistics"
    introductory_linear_algebra = "Introductory Linear Algebra"
    introductory_calculus = "Introductory Calculus"

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
    hots = "Higher Order Thinking Skills"

class Explanation(BaseModel):
    title: str
    content: str

class Formula(BaseModel):
    title: str
    code: str

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