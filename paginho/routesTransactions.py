from fastapi import FastAPI, Depends
from pgDatabase import get_db
from sqlalchemy.orm import Session
from schemas import PostTransactionSchema, GetTransactionSchema
import crud
from fastapi import APIRouter, HTTPException, status
from redis_file import get_cbu

router = APIRouter()

# GET /transactions
# TODO:
@router.get("/", status_code= status.HTTP_200_OK)
async def get_transactions(request: GetTransactionSchema, db: Session = Depends(get_db)):
    if not request.is_valid():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email is not valid")
    if not crud.validate_user(db, request.email, request.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    return crud.get_transactions_by_email(db, request.email, request.limit)
    

# POST /transactions
#TODO: Validar parametros
@router.post("/", status_code= status.HTTP_201_CREATED)
async def create_transaction(request: PostTransactionSchema, db: Session = Depends(get_db)):
    if not request.is_valid():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "One or more fields is not valid")
    if not crud.validate_user(db, request.email, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    cbuTo = get_cbu(request.key)
    if not cbuTo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Key not found")
    # TODO: Resolver transaccion con bancos
    return crud.create_transaction(db, cbuFrom=request.cbu, cbuTo=cbuTo, amount=request.amount)