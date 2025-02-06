from sqlalchemy.orm import Session
from src.config.database import SessionLocal, engine
from src.models.quiz_models import Base



def initialize_database():
    Base.metadata.create_all(bind=engine)