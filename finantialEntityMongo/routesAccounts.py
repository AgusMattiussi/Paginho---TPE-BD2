from fastapi import APIRouter, HTTPException, status
from mongoDatabase import get_db
from schemas import AccountDTO
from pymongo.errors import PyMongoError
import crud

CBU_LENGTH = 22
COLLECTION_NAME = "BankAccount"

router = APIRouter()

collection = get_db()[COLLECTION_NAME]


# GET /accounts/{cbu}
@router.get("/{cbu}")
async def get_account(cbu: str):
    if len(cbu) != CBU_LENGTH:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CBU length must be 22 characters")
    
    try:
        accounts = crud.get_account(cbu, collection)
        if accounts:
            account = accounts[0]
            return AccountDTO(name=account['name'], email=account['email'], cuit=account['cuit'], telephone=account['phoneNumber'], balance=account['balance'])
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)