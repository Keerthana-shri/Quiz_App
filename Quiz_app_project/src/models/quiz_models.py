from sqlalchemy import Column, Integer, String, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from src.utils.init_db import Base

class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    topic = Column(String, nullable=False, index=True)
    difficulty = Column(String, nullable=False, index=True)
    timer = Column(Integer, nullable=True)

    questions = relationship("Question", back_populates="quiz", cascade="all, delete")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    question_type = Column(String, nullable=False)
    options = Column(String, nullable=False)
    correct_answer = Column(String, nullable=False)
    explanation = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'), nullable=False)

    quiz = relationship("Quiz", back_populates="questions")
