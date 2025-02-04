from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.schemas.auth_schemas import UserCreate, UserResponse, Token
from src.models.auth_models import User as UserModel
from src.config.database import get_db
from src.services.auth_services import create_access_token, verify_password, get_password_hash
from src.utils.dependencies import get_current_user

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    new_user = UserModel(username=user.username, hashed_password=hashed_password, role=user.role.value)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    access_token = create_access_token({"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/user", response_model=UserResponse)
def get_current_user_info(current_user: UserResponse = Depends(get_current_user)):
    return current_user