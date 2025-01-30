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

class QuestionOptionSchema(BaseModel):
    option_text: str
    is_correct: bool

    class Config:
        orm_mode = True

class QuestionSchema(BaseModel):
    text: str
    question_type: QuestionType
    correct_answer: str
    explanation: Optional[str] = None
    image_url: Optional[str] = None
    options: List[QuestionOptionSchema] = [] 
    quiz_id: int

    class Config:
        orm_mode = True

class QuestionCreate(QuestionSchema):
    pass

class QuestionUpdate(BaseModel):
    text: Optional[str]
    question_type: Optional[QuestionType]
    correct_answer: Optional[str]
    explanation: Optional[str] = None
    image_url: Optional[str] = None
    options: List[QuestionOptionSchema] = [] 
    quiz_id: int

    class Config:
        orm_mode = True

class QuestionResponse(QuestionSchema):
    pass

class QuizSchema(BaseModel):
    title: str
    topic: str
    difficulty: DifficultyLevel
    timer: int 

    class Config:
        orm_mode = True

class QuizCreate(QuizSchema):
    pass

class QuizUpdate(BaseModel):
    title: Optional[str]
    topic: Optional[str]
    difficulty: Optional[DifficultyLevel]
    timer: Optional[int]

    class Config:
        orm_mode = True

class QuizResponse(QuizSchema):
    id: int