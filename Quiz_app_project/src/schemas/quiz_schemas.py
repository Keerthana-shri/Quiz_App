from pydantic import BaseModel
from typing import Optional, List, Dict
from enum import Enum
from datetime import datetime

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
    is_correct: Optional[bool] = None

    class Config:
        orm_mode = True
        from_attributes = True

class QuestionOptionCandidateSchema(BaseModel):
    option_text: str

    class Config:
        orm_mode = True
        from_attributes = True

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
        from_attributes = True

class QuestionCandidateSchema(BaseModel):
    text: str
    question_type: QuestionType
    image_url: Optional[str] = None
    options: List[QuestionOptionCandidateSchema] = []
    quiz_id: int

    class Config:
        orm_mode = True
        from_attributes = True

class QuestionCreate(QuestionSchema):
    pass

class QuestionUpdate(BaseModel):
    text: Optional[str]
    question_type: Optional[QuestionType]
    correct_answer: Optional[str]
    explanation: Optional[str] = None
    image_url: Optional[str] = None
    options: List[QuestionOptionSchema] = []
    quiz_id: Optional[int]

    class Config:
        orm_mode = True
        from_attributes = True

class QuestionResponse(QuestionSchema):
    pass

class QuestionCandidateResponse(QuestionCandidateSchema):
    pass

class QuizSchema(BaseModel):
    title: str
    topic: str
    difficulty: DifficultyLevel
    timer: int 

    class Config:
        orm_mode = True
        from_attributes = True

class QuizCreate(QuizSchema):
    pass

class QuizUpdate(BaseModel):
    title: Optional[str] =None
    topic: Optional[str] =None
    difficulty: Optional[DifficultyLevel] =None
    timer: Optional[int] =None

    class Config:
        orm_mode = True
        from_attributes = True

class QuizResponse(QuizSchema):
    id: int
    questions: List[QuestionResponse]

    class Config:
        orm_mode = True
        from_attributes = True

class QuizCandidateResponse(QuizSchema):
    id: int
    questions: List[QuestionCandidateResponse]

    class Config:
        orm_mode = True
        from_attributes = True

class QuizAttemptCreate(BaseModel):
    answers: dict

    class Config:
        orm_mode = True
        from_attributes = True

class QuizAttemptBaseResponse(BaseModel):
    id: int
    candidate_id: int
    quiz_id: int
    attempt_number: int
    timestamp: datetime
    start_time: datetime
    end_time: datetime
    answers: Dict[str, str]

    class Config:
        orm_mode = True
        from_attributes = True

class QuizAttemptDetailedResponse(QuizAttemptBaseResponse):
    score: Optional[float]
    correct_answers: Optional[int]
    wrong_answers: Optional[int]

    class Config:
        orm_mode = True
        from_attributes = True

