from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from pgDatabase import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import BasicAuthSchema, LinkedAccountsPostSchema, LinkedAccountsPutSchema
import crud

CBU_LENGTH = 22

router = APIRouter()

# GET /linkedAccounts
@router.get("/")
async def get_linked_accounts(request: BasicAuthSchema, db: Session = Depends(get_db)):  
    try:
        linkedAccounts = crud.get_linked_entities(db, user=request)
        if linkedAccounts:
            return linkedAccounts
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Linked account not found")
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# POST /linkedAccounts
@router.post("/")
async def create_linked_account(request: LinkedAccountsPostSchema, db: Session = Depends(get_db)):
    if len(request.cbu) != CBU_LENGTH:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CBU length must be 22 characters")
    
    try:
        linkedAccounts = crud.create_linked_entity(db, user=request)
        if linkedAccounts:
            return linkedAccounts
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Linked account not found")
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)    

# PUT /linkedAccounts/{cbu}
@router.put("/{cbu}")
async def modify_linked_account(cbu: str, request: LinkedAccountsPutSchema, db: Session = Depends(get_db)):
    if len(cbu) != CBU_LENGTH:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CBU length must be 22 characters")
    
    try:
        linkedAccount = crud.modify_linked_account(cbu, db, user=request)
        if linkedAccount:
            return linkedAccount
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Linked account not found")
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# GET /linkedAccounts/{cbu}
# TODO:
@router.get("/{CBU}")
async def get_linked_account(request: BasicAuthSchema, db: Session = Depends(get_db)):
    return {"message" : "To be implemented"}