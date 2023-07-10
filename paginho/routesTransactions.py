from fastapi import FastAPI, Depends
from pgDatabase import get_db
from sqlalchemy.orm import Session
from schemas import PostTransactionSchema, GetTransactionSchema, TransactionDTO, TransactionListDTO
from fastapi import APIRouter, HTTPException, status
from redisDatabase import get_cbu

import crud, financialEntities

router = APIRouter()

# GET /transactions
# TODO:
@router.get("/",  status_code=status.HTTP_200_OK)
async def get_transactions(request: GetTransactionSchema, db: Session = Depends(get_db)):
    if not request.is_valid():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "One or more fields is not valid")
    if not crud.validate_user(db, request.email, request.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    
    transactionList = crud.get_transactions_by_email(db, request.email, request.limit)
    DTOList = []

    for transaction in transactionList:
        DTOList.append(TransactionDTO(cbuFrom=transaction.cbuFrom, cbuTo=transaction.cbuTo, amount=transaction.amount, date=str(transaction.time)))
    return TransactionListDTO(transactions=DTOList)
    

# POST /transactions
#TODO: Validar parametros
@router.post("/",  status_code=status.HTTP_201_CREATED)
async def create_transaction(request: PostTransactionSchema, db: Session = Depends(get_db)):
    if not request.is_valid():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "One or more fields is not valid")
    if not crud.validate_user(db, request.email, request.password, request.cbu):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    
    cbuTo = None
    try:
        cbuTo = get_cbu(request.key)
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Error getting key")
    if not cbuTo:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Key not found")
    
    try:
        financialEntities.bank_transaction(db, request.cbu, cbuTo, float(request.amount))
    except financialEntities.UnregisteredEntityException:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "One of the financial entities is unreachable")
    except HTTPException as e:
        raise
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,"Internal Server Error")

    try:
        transaction = crud.create_transaction(db, cbuFrom=request.cbu, cbuTo=cbuTo, amount=request.amount)
        return TransactionDTO(cbuFrom=transaction.cbuFrom, cbuTo=transaction.cbuTo, amount=transaction.amount, date=str(transaction.time))
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,"Internal Server Error")
