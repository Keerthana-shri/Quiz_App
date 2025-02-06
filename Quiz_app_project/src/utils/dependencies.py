from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from src.config.settings import app_config
from src.config.database import get_db
from src.models.quiz_models import User, UserRole

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

def get_current_user(db: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    try:
        payload = jwt.decode(token, app_config["SECRET_KEY"], algorithms=[app_config["ALGORITHM"]])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

def get_current_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

def get_current_candidate(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.CANDIDATE.value:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user