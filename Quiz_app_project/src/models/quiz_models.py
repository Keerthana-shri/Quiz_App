from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, Float, DateTime, JSON
from sqlalchemy.orm import relationship
from src.utils.init_db import Base
from datetime import datetime

class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    topic = Column(String, index=True, nullable=False)
    difficulty = Column(String, index=True, nullable=False)
    timer = Column(Integer, nullable=False)
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")
    quiz_attempts = relationship("QuizAttempt", back_populates="quiz")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    text = Column(Text, nullable=False)
    question_type = Column(String, nullable=False)
    correct_answer = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    quiz = relationship("Quiz", back_populates="questions")
    options = relationship("QuestionOption", back_populates="question", cascade="all, delete-orphan")

class QuestionOption(Base):
    __tablename__ = "question_options"
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    option_text = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False, default=False)
    question = relationship("Question", back_populates="options")

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    score = Column(Float, nullable=True)
    correct_answers = Column(Integer, nullable=True)
    wrong_answers = Column(Integer, nullable=True)
    attempt_number = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    start_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    answers = Column(JSON, nullable=True)

    candidate = relationship("User", back_populates="quiz_attempts")
    quiz = relationship("Quiz", back_populates="quiz_attempts")

