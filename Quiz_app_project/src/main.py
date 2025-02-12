from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from src.utils.dependencies import JWTBearer
from src.utils.init_db import initialize_database
from src.routes.api import api_router

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="src/frontend"), name="static")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend's URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    initialize_database()

@app.get("/", dependencies=[Depends(JWTBearer())])
def read_root():
    return {"message": "Welcome to the Quiz App!"}

app.include_router(api_router)