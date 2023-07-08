from fastapi import APIRouter, HTTPException, Path
from fastapi import Depends
from pgDatabase import get_db
from sqlalchemy.orm import Session
from schemas import UserSchema, TestSchema

import crud

router = APIRouter()
# GET /users
# POST /users

@router.get("/")
async def get_user(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_user(db, skip, limit)

@router.post("/")
async def create_user(request: UserSchema, db: Session = Depends(get_db)):
    return crud.create_user(db, user=request)





