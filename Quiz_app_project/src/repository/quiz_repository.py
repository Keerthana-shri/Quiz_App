from sqlalchemy.orm import Session
from src.models.quiz_models import Quiz, Question, QuestionOption, QuizAttempt
from src.schemas.quiz_schemas import QuizCreate, QuestionCreate, QuizUpdate, QuestionUpdate

class QuizRepository:
    def create_quiz(self, db: Session, quiz: QuizCreate):
        db_quiz = Quiz(
            title=quiz.title,
            topic=quiz.topic,
            difficulty=quiz.difficulty.value,
            timer=quiz.timer
        )
        db.add(db_quiz)
        db.commit()
        db.refresh(db_quiz)
        return db_quiz

    def get_quiz_by_title(self, db: Session, title: str):
        return db.query(Quiz).filter(Quiz.title == title).first()

    def get_quiz_by_id(self, db: Session, quiz_id: int):
        return db.query(Quiz).filter(Quiz.id == quiz_id).first()

    def update_quiz(self, db: Session, quiz_id: int, quiz_update: QuizUpdate):
        quiz = self.get_quiz_by_id(db, quiz_id)
        if not quiz:
            return None
        for key, value in quiz_update.dict(exclude_unset=True).items():
            setattr(quiz, key, value)
        db.commit()
        db.refresh(quiz)
        return quiz

    def delete_quiz(self, db: Session, quiz_id: int):
        quiz = self.get_quiz_by_id(db, quiz_id)
        if not quiz:
            return False
        questions = db.query(Question).filter(Question.quiz_id == quiz_id).all()
        for question in questions:
            db.query(QuestionOption).filter(QuestionOption.question_id == question.id).delete()
            db.delete(question)
        db.delete(quiz)
        db.commit()
        return True
    
class QuestionRepository:
    def create_question(self, db: Session, question: QuestionCreate):
        db_question = Question(
            text=question.text,
            question_type=question.question_type.value,  
            correct_answer=question.correct_answer,
            explanation=question.explanation,
            image_url=question.image_url,
            quiz_id=question.quiz_id
        )
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        
        for option in question.options:
            is_correct = option.is_correct if 'is_correct' in option else (option.option_text == question.correct_answer)
            db_option = QuestionOption(
                option_text=option.option_text,
                is_correct=is_correct,
                question_id=db_question.id
            )
            db.add(db_option)
        
        db.commit()
        db.refresh(db_question)
        return db_question

    def update_question(self, db: Session, question_id: int, question_update: QuestionUpdate):
        question = self.get_question_by_id(db, question_id)
        if not question:
            return None
        for key, value in question_update.dict(exclude_unset=True).items():
            if key == "options":
                db.query(QuestionOption).filter(QuestionOption.question_id == question_id).delete()
                for option in value:
                    is_correct = option["is_correct"] if 'is_correct' in option else (option["option_text"] == question_update.correct_answer)
                    db_option = QuestionOption(
                        option_text=option["option_text"],
                        is_correct=is_correct,
                        question_id=question_id
                    )
                    db.add(db_option)
            else:
                setattr(question, key, value)
        
        db.commit()
        db.refresh(question)
        return question

    def delete_question(self, db: Session, question_id: int):
        question = self.get_question_by_id(db, question_id)
        if not question:
            return False
        db.query(QuestionOption).filter(QuestionOption.question_id == question_id).delete()
        db.delete(question)
        db.commit()
        return True

    def get_question_by_id(self, db: Session, question_id: int):
        return db.query(Question).filter(Question.id == question_id).first()

    def get_question_by_text_and_quiz(self, db: Session, text: str, quiz_id: int):
        return db.query(Question).filter(Question.text == text, Question.quiz_id == quiz_id).first()

class QuizAttemptRepository:
    def create_quiz_attempt(self, db: Session, candidate_id: int, quiz_id: int, score: float):
        db_quiz_attempt = QuizAttempt(candidate_id=candidate_id, quiz_id=quiz_id, score=score)
        db.add(db_quiz_attempt)
        db.commit()
        db.refresh(db_quiz_attempt)
        return db_quiz_attempt

    def get_quiz_attempts_by_candidate(self, db: Session, candidate_id: int):
        return db.query(QuizAttempt).filter(QuizAttempt.candidate_id == candidate_id).all()