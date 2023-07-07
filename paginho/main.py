from fastapi import FastAPI, APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from models import User
from database import SessionLocal, get_db
#from paginhoApi import router
from schemas import UserSchema
import crud

app = FastAPI()
router = APIRouter()

app.include_router(router, prefix="/users", tags=["users"])



@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users")
async def get_user(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_user(db, skip, limit)

@app.post("/users")
async def create_user(request: UserSchema, db: Session = Depends(get_db)):
    return crud.create_user(db, user=request)