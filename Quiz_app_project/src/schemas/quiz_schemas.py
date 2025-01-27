from pydantic import BaseModel
from typing import Optional, List

class QuestionBase(BaseModel):
    text: str
    question_type: str
    options: Optional[str]
    correct_answer: str
    explanation: Optional[str]
    image_url: Optional[str]

class QuestionCreate(QuestionBase):
    quiz_id: int

class QuestionResponse(QuestionBase):
    id: int

    class Config:
        orm_mode = True

class QuizBase(BaseModel):
    title: str
    description: Optional[str]
    topic: str
    difficulty: str
    timer: Optional[int]

class QuizCreate(QuizBase):
    pass

class QuizResponse(QuizBase):
    id: int
    questions: List[QuestionResponse] = []

    class Config:
        orm_mode = True
