from fastapi import FastAPI, Depends
from pgDatabase import get_db
from sqlalchemy.orm import Session
from schemas import TestSchema
import crud
from fastapi import APIRouter

router = APIRouter()

# GET /transactions
# TODO:
@router.get("/trans")
async def get_transactions(request: None, db: Session = Depends(get_db)):
    return {"message" : "To be implemented"}

# POST /transactions
@router.post("/trans")
async def create_transaction(request: TestSchema, db: Session = Depends(get_db)):
    return crud.create_transaction(db, cbuFrom=request.cbu1, cbuTo=request.cbu2, amount=request.amount)