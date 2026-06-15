from fastapi import FastAPI
from backend.routes import (
    home,
    auth
)
from backend.routes.api import (
    get_topics,
    explination,
    examples,
    questions
)

# App Instance
app = FastAPI()

# Including Routes
app.include_router(home.app)
app.include_router(auth.app)

app.include_router(get_topics.app)
app.include_router(explination.app)
app.include_router(examples.app)
app.include_router(questions.app)