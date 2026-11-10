import os

APP_NAME = "MathLab"
API_BASE_URL = "http://127.0.0.1:3000"
DEMO_USERNAME = os.getenv("MATHAPI_DEMO_USERNAME", "demo_project")
DEMO_EMAIL = os.getenv("MATHAPI_DEMO_EMAIL", "demo_project@example.com")

REQUEST_TIMEOUT = 20
TOPICS_TTL = 600
CONTENT_TTL = 1800
DAILY_TTL = 3600

BRANCHES = [
    "Number Theory",
    "Algebra",
    "Geometry",
    "Coordinate Geometry",
    "Trigonometry",
    "Combinatorics",
    "Applied Mathematics",
]

DIFFICULTIES = [
    "Beginner",
    "Intermediate",
    "Advanced",
]

QUESTION_TYPES = [
    "Conceptual",
    "Numerical",
    "To Prove",
    "Word Problem",
    "Case Based",
    "Higher Order Thinking Skills",
]
