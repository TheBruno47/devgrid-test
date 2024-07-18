from fastapi import FastAPI
from app.routers import weather

app = FastAPI()

app.include_router(weather.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}