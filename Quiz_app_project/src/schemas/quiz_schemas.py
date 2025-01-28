from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class QuestionType(str, Enum):
    MCQ = "MCQ"
    TRUE_FALSE = "True/False"
    FILL_IN_THE_BLANKS = "Fill in the Blanks"

class DifficultyLevel(str, Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"

class QuestionBase(BaseModel):
    text: str
    question_type: QuestionType
    options: str
    correct_answer: str
    explanation: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        orm_mode = True

class QuestionCreate(BaseModel):
    text: str
    question_type: QuestionType
    options: str
    correct_answer: str
    explanation: Optional[str]
    image_url: Optional[str]
    quiz_id: int

class QuestionUpdate(BaseModel):
    text: Optional[str]
    question_type: Optional[QuestionType]
    options: Optional[str]
    correct_answer: Optional[str]
    explanation: Optional[str]
    image_url: Optional[str]

    class Config:
        orm_mode = True

class QuestionResponse(BaseModel):
    id: int
    text: str
    question_type: QuestionType
    options: str
    correct_answer: str
    explanation: Optional[str]
    image_url: Optional[str]
    quiz_id: int

    class Config:
        orm_mode = True

class QuizBase(BaseModel):
    title: str
    description: Optional[str]
    topic: str
    difficulty: DifficultyLevel
    timer: Optional[int]

    class Config:
        orm_mode = True

class QuizCreate(QuizBase):
    pass

class QuizUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    topic: Optional[str]
    difficulty: Optional[DifficultyLevel]
    timer: Optional[int]

    class Config:
        orm_mode = True

class QuizResponse(QuizBase):
    id: int
    questions: List[QuestionResponse] = []

    class Config:
        orm_mode = True

