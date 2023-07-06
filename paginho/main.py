from fastapi import FastAPI, APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from models import User
from database import SessionLocal
#from paginhoApi import router
from schemas import UserSchema
import crud

app = FastAPI()
router = APIRouter()

app.include_router(router, prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.post("/users")
async def create_user(request: UserSchema, db: Session = Depends(get_db)):
    crud.create_user(db, user=request)
    return