from fastapi import FastAPI
from sqlalchemy.orm import Session
from src.config.database import SessionLocal, engine
from src.models.base import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Quiz App!"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()