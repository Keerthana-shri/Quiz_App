from pydantic import BaseModel, Field
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    CANDIDATE = "candidate"

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    role: UserRole = Field(default=UserRole.CANDIDATE)  # Set "candidate" as default

class UserSchema(UserBase):
    id: int
    role: UserRole

    class Config:
        from_attributes = True

class UserResponse(UserSchema):
    pass 

class Token(BaseModel):
    access_token: str
    token_type: str
