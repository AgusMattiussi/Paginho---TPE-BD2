from mongoDatabase import get_bankAccount_collection, get_transaction_collection
from schemas import TransactionSchema, TransactionDTO
from fastapi import APIRouter, HTTPException, status
from pymongo.errors import PyMongoError
import crud

router = APIRouter()

# POST /transactions
@router.post("/")
async def create_transaction(request: TransactionSchema):
    bankAccountCollection = get_bankAccount_collection()

    if not crud.validate_account(request.cbuFrom, bankAccountCollection):
        raise HTTPException(status_code=404, detail="Account does not belong to this bank")

    if not crud.validate_account(request.cbuTo, bankAccountCollection):
        #TODO: llamar a paginhoAPI para hacer la transaccion
        raise HTTPException(status_code=404, detail="Account not found")

    try:
        transactions = crud.create_transaction(get_transaction_collection(), cbuFrom=request.cbuFrom, cbuTo=request.cbuTo, amount=request.amount)
        if transactions:
            transaction = transactions[0]
            return TransactionDTO(timestamp=str(transaction['time']), cbuFrom=transaction['cbuFrom'], cbuTo=transaction['cbuTo'], amount=transaction['amount'])
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error creating transaction")
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)