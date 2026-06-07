from pydantic import BaseModel
from enum import Enum
from typing import List

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
    mathematical_reasoning = "Mathematical Reasoning"

class Difficulty(Enum):
    beginner = "Beginner"
    intermediate = "Intermediate"
    advanced = "Advanced"

class Topic(BaseModel):
    _id: str
    name: str
    branch: Branch
    difficulty: Difficulty
    questions_available: int
    learning_sources_available: int

class Topics(BaseModel):
    topics: List[Topic]