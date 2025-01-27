from sqlalchemy.orm import Session
from src.config.database import SessionLocal, engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def initialize_database():
    Base.metadata.create_all(bind=engine)