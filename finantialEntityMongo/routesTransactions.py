from mongoDatabase import get_db
from schemas import TransactionSchema, TransactionDTO
from fastapi import APIRouter, HTTPException, status, Depends
import crud

router = APIRouter()

# POST /transactions
@router.post("/")
async def create_transaction(request: TransactionSchema):
    # if not crud.validate_account(request.cbuFrom, db):
    #     raise HTTPException(status_code=404, detail="Account does not belong to this bank")

    # if not crud.validate_account(request.cbuTo, db):
    #     #TODO: llamar a paginhoAPI para hacer la transaccion
    #     raise HTTPException(status_code=404, detail="Account not found")

    # try:
    #     transaction = crud.create_transaction(db['Transactions'], cbuFrom=request.cbuFrom, cbuTo=request.cbuTo, amount=request.amount)
    #     if transaction:
    #         return TransactionDTO(timestamp=str(transaction.time), cbuFrom=transaction.cbuFrom, cbuTo=transaction.cbuTo, amount=transaction.amount)
    #     else:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error creating transaction")
    # except Exception as e:
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return {"TO": "DO"}