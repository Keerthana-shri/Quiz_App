from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from src.utils.init_db import Base

class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    topic = Column(String, index=True, nullable=False)
    difficulty = Column(String, index=True, nullable=False)
    timer = Column(Integer, nullable=False)  # Added timer field
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    text = Column(Text, nullable=False)
    question_type = Column(String, nullable=False)  # MCQ, True/False, Fill in the Blanks
    correct_answer = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)  # Added explanation field
    image_url = Column(String, nullable=True)
    quiz = relationship("Quiz", back_populates="questions")
    options = relationship("QuestionOption", back_populates="question")

class QuestionOption(Base):
    __tablename__ = "question_options"
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    option_text = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False, default=False)  # Added is_correct field
    question = relationship("Question", back_populates="options")