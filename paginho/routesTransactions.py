from fastapi import FastAPI, Depends
from pgDatabase import get_db
from sqlalchemy.orm import Session
from schemas import PostTransactionSchema, GetTransactionSchema
import crud
from fastapi import APIRouter, HTTPException, status

router = APIRouter()

# GET /transactions
# TODO:
@router.get("/")
async def get_transactions(request: GetTransactionSchema, db: Session = Depends(get_db)):
    if not crud.validate_user(db, request.email, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return crud.get_transactions_by_email(db, request.email, request.limit)
    

# POST /transactions
#TODO: Validar parametros
@router.post("/")
async def create_transaction(request: PostTransactionSchema, db: Session = Depends(get_db)):
    if not crud.validate_user(db, request.email, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # TODO: Redis: request.key -> cbuTo
    cbuTo = "2850590940090418135201"
    # TODO: Resolver transaccion con bancos
    return crud.create_transaction(db, cbuFrom=request.cbu, cbuTo=cbuTo, amount=request.amount)