from pgDatabase import get_db
from sqlalchemy.orm import Session
from schemas import TransactionSchema, TransactionDTO
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import crud

router = APIRouter()

# POST /transactions
@router.post("/")
async def create_transaction(request: TransactionSchema, db: Session = Depends(get_db)):
    if not crud.validate_account(request.cbuFrom, db):
        raise HTTPException(status_code=404, detail="Account does not belong to this bank")

    if not crud.validate_account(request.cbuTo, db):
        #TODO: llamar a paginhoAPI para hacer la transaccion
        raise HTTPException(status_code=404, detail="Account not found")

    try:
        transaction = crud.create_transaction(db, cbuFrom=request.cbuFrom, cbuTo=request.cbuTo, amount=request.amount)
        if transaction:
            return TransactionDTO(timestamp=str(transaction.time), cbuFrom=transaction.cbuFrom, cbuTo=transaction.cbuTo, amount=transaction.amount)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error creating transaction")
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    