from fastapi import FastAPI, Depends
from pgDatabase import get_db
from sqlalchemy.orm import Session
from schemas import PostTransactionSchema
import crud
from fastapi import APIRouter, HTTPException, status
from redis_file import get_user_cbu_by_key

router = APIRouter()

# GET /transactions
# TODO:
@router.get("/")
async def get_transactions(request: None, db: Session = Depends(get_db)):
    return {"message" : "To be implemented"}

# POST /transactions
#TODO: Validar parametros
@router.post("/")
async def create_transaction(request: PostTransactionSchema, db: Session = Depends(get_db)):
    if not crud.validate_user(db, request.email, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # TODO: Redis: request.key -> cbuTo
    cbuTo = get_user_cbu_by_key(request.key)
    if not cbuTo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Key not found")
    # cbuTo = "2850590940090418135201"
    # TODO: Resolver transaccion con bancos
    return crud.create_transaction(db, cbuFrom=request.cbu, cbuTo=cbuTo, amount=request.amount)