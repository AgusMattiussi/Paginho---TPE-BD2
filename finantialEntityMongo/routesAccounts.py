from fastapi import APIRouter, HTTPException, status
from mongoDatabase import get_db
from schemas import AccountDTO
import crud

CBU_LENGTH = 22

router = APIRouter()

# GET /accounts/{cbu}
@router.get("/{cbu}")
async def get_account(cbu: str, db: get_db()):
    if len(cbu) != CBU_LENGTH:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CBU length must be 22 characters")
    
    try:
        account = crud.get_account(cbu, db['BankAccounts'])
        if account:
            return AccountDTO(name=account.name, email=account.email, cuit=account.cuit, telephone=account.phoneNumber, balance=account.balance)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)