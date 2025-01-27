from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from src.config.settings import app_config
 
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
 
    async def __call__(self, request: Request):
        credentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
 
    def verify_jwt(self, token: str) -> bool:
        try:
            payload = jwt.decode(token, app_config["SECRET_KEY"], algorithms=app_config["ALGORITHM"])
            print("Decoded Payload:", payload)  
            return True
        except JWTError:
            return False

# from passlib.context import CryptContext
# from jose import jwt, JWTError
# from datetime import datetime, timedelta
# from fastapi import HTTPException, Depends
# from fastapi.security import OAuth2PasswordBearer
# from sqlalchemy.orm import Session
# from src.models.quiz_models import User
# from src.config.database import get_db

# # Password hashing
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# SECRET_KEY = "your_secret_key"  # Replace with a secure key
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# def hash_password(password: str) -> str:
#     return pwd_context.hash(password)

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)

# # JWT utilities
# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise HTTPException(status_code=401, detail="Invalid authentication credentials")
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid authentication credentials")
   
#     user = db.query(User).filter(User.email == email).first()
#     if user is None:
#         raise HTTPException(status_code=401, detail="Invalid authentication credentials")
#     return user