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

    if not crud.validate_account(request.cbuFrom, bankAccountCollection):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account does not belong to this bank")

    if not crud.validate_account(request.cbuTo, bankAccountCollection):
        #TODO: llamar a paginhoAPI para hacer la transaccion
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    try:
        transactions = crud.create_transaction(get_transaction_collection(), cbuFrom=request.cbuFrom, cbuTo=request.cbuTo, amount=request.amount)
        if transactions:
            transaction = transactions[0]
            return TransactionDTO(timestamp=str(transaction['time']), cbuFrom=transaction['cbuFrom'], cbuTo=transaction['cbuTo'], amount=transaction['amount'])
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error creating transaction")
    except PyMongoError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)