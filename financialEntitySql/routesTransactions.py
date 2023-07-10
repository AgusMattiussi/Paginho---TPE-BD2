from pgDatabase import get_db
from sqlalchemy.orm import Session
from schemas import TransactionSchema, TransactionDTO
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.exc import SQLAlchemyError
import crud

router = APIRouter()

# POST /transactions
@router.post("/", status_code= status.HTTP_201_CREATED)
async def create_transaction(request: TransactionSchema, db: Session = Depends(get_db)):
    if not request.is_valid():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "One or more fields is not valid")

    cbuFromValidation = crud.validate_account(request.cbuFrom, db)
    cbuToValidation = crud.validate_account(request.cbuTo, db)

    if not cbuFromValidation and not cbuToValidation:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Account does not belong to this bank")

    multiple_bank_transaction = 0 # Hacer un enum

    if cbuFromValidation and not cbuToValidation: # Resto plata al cbuTo 
        multiple_bank_transaction = 1

    if not cbuFromValidation and cbuToValidation: # Sumo plata al cbuTo
        multiple_bank_transaction = 2

    try:
        transaction = crud.create_transaction(db, cbuFrom=request.cbuFrom, cbuTo=request.cbuTo, amount=request.amount, multiple_bank_transaction=multiple_bank_transaction)
        if transaction:
            return TransactionDTO(timestamp=str(transaction.time), cbuFrom=transaction.cbuFrom, cbuTo=transaction.cbuTo, amount=transaction.amount)
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Error creating transaction")
    except crud.NotEnoughFundsException:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Account does not have enough funds to make the transaction")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    