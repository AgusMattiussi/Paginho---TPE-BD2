from fastapi import APIRouter, HTTPException, Path, status, Depends
from pgDatabase import get_db
from sqlalchemy.orm import Session
from schemas import UserSchema, TestSchema

import crud

router = APIRouter()


# GET /users
@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_user(db, skip, limit)

# POST /users
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(request: UserSchema, db: Session = Depends(get_db)):
    return crud.create_user(db, user=request)

#TODO: DELETE /users?



