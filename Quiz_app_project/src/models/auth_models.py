from sqlalchemy import Column, Integer, String
from src.utils.init_db import Base
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    CANDIDATE = "candidate"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, nullable=False, default=UserRole.CANDIDATE.value)  # Default role as "candidate"
