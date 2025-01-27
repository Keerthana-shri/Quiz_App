from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from src.utils.init_db import Base

class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    topic = Column(String, index=True)
    difficulty = Column(String, index=True)
    timer = Column(Integer, nullable=True)

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    text = Column(Text, nullable=False)
    question_type = Column(String, nullable=False)  # MCQ, True/False, Fill in the Blanks
    options = Column(Text, nullable=True)  # JSON string for MCQ options
    correct_answer = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)

    quiz = relationship("Quiz", back_populates="questions")

Quiz.questions = relationship("Question", back_populates="quiz")