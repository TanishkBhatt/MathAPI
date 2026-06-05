from fastapi import APIRouter, status

app = APIRouter()

@app.get("/", status_code=status.HTTP_200_OK)
async def home():
    return {"message": "Application Succesfully Connected!"}