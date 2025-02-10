from fastapi import FastAPI, Depends
from src.utils.dependencies import JWTBearer
from pydantic import ValidationError
from src.utils.init_db import initialize_database
from src.routes.api import api_router
from fastapi.security import OAuth2PasswordBearer
app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.on_event("startup")
async def startup_event():
    initialize_database()

@app.get("/", dependencies=[Depends(JWTBearer())])
def read_root():
    return {"message": "Welcome to the Quiz App!"}

app.include_router(api_router)