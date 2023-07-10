from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from pgDatabase import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import AccountDTO
import crud
import validators

CBU_LENGTH = 22

router = APIRouter()

# GET /accounts/{cbu}
@router.get("/{cbu}", status_code= status.HTTP_200_OK)
async def get_account(cbu: str, db: Session = Depends(get_db)):
    if not validators.validate_cbu(cbu):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CBU length must be 22 characters")
    
    try:
        account = crud.get_account(cbu, db)
        if account:
            return AccountDTO(name=account.name, email=account.email, cuit=account.cuit, telephone=account.phoneNumber, balance=account.balance)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)