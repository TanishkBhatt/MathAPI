from fastapi import FastAPI
from backend.routes import home

# App Instance
app = FastAPI()

# Including Routes
app.include_router(home.app)