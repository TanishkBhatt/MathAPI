from fastapi import FastAPI
from routes import home

# Application Instance
app = FastAPI()

# Adding Routes
app.include_router(home.app)