from mongoDatabase import get_bankAccount_collection, get_transaction_collection
from schemas import TransactionSchema, TransactionDTO
from fastapi import APIRouter, HTTPException, status
from pymongo.errors import PyMongoError

import crud

router = APIRouter()

# POST /transactions
@router.post("/", status_code= status.HTTP_201_CREATED)
async def create_transaction(request: TransactionSchema):
    if not request.is_valid():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="One or more fields is not valid")

    bankAccountCollection = get_bankAccount_collection()
    cbuFromValidation = crud.validate_account(request.cbuFrom, bankAccountCollection)
    cbuToValidation = crud.validate_account(request.cbuTo, bankAccountCollection)

    if not cbuFromValidation and not cbuToValidation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account does not belong to this bank")

    multiple_bank_transaction = 0 # Hacer un enum

    if cbuFromValidation and not cbuToValidation: # Resto plata al cbuTo 
        multiple_bank_transaction = 1

    if not cbuFromValidation and cbuToValidation: # Sumo plata al cbuTo
        multiple_bank_transaction = 2

    try:
        transactions = crud.create_transaction(get_transaction_collection(), cbuFrom=request.cbuFrom, cbuTo=request.cbuTo, amount=float(request.amount), multiple_bank_transaction=multiple_bank_transaction)
        if transactions:
            transaction = transactions[0]
            return TransactionDTO(timestamp=str(transaction['time']), cbuFrom=transaction['cbuFrom'], cbuTo=transaction['cbuTo'], amount=transaction['amount'])
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error creating transaction")
    except crud.NotEnoughFundsException:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Account does not have enough funds to make the transaction")
    except PyMongoError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)