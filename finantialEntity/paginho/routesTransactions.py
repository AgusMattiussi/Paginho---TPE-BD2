from fastapi import FastAPI, Depends
from pgDatabase import get_db
from sqlalchemy.orm import Session
from schemas import TransactionSchema
import crud
from fastapi import APIRouter, HTTPException, status

router = APIRouter()

# POST /transactions
@router.post("/")
async def create_transaction(request: TransactionSchema, db: Session = Depends(get_db)):
    return crud.create_transaction(db, cbuFrom=request.cbu, cbuTo=request.cbuTo, amount=request.amount)