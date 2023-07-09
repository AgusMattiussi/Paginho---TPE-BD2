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
@router.get("/", status_code=status.HTTP_200_OK)
async def get_linked_accounts(request: BasicAuthSchema, db: Session = Depends(get_db)):
    if not request.is_valid():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email is not valid")
    if not crud.validate_user(db, request.email, request.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")

    try:
        linkedAccounts = crud.get_linked_entities(db, user=request)
        if linkedAccounts:
            return linkedAccounts
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Linked account not found")
    except SQLAlchemyError as error:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

# POST /linkedAccounts
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_linked_account(request: LinkedAccountsPostSchema, db: Session = Depends(get_db)):
    if not request.is_valid():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "One or more fields is not valid")
    if not crud.validate_user(db, request.email, request.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    if len(request.cbu) != CBU_LENGTH:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "CBU length must be 22 characters")
    
    try:
        linkedAccounts = crud.create_linked_entity(db, user=request)
        if linkedAccounts:
            return linkedAccounts
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Linked account not found")
    except SQLAlchemyError as error:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)    

# PUT /linkedAccounts/{cbu}
@router.put("/{cbu}", status_code=status.HTTP_200_OK)
async def modify_linked_account(cbu: str, request: LinkedAccountsPutSchema, db: Session = Depends(get_db)):
    if not request.is_valid():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "One or more fields is not valid")
    if not crud.validate_user(db, request.email, request.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    if len(cbu) != CBU_LENGTH:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "CBU length must be 22 characters")
    
    try:
        linkedAccount = crud.modify_linked_account(cbu, db, user=request)
        if linkedAccount:
            return linkedAccount
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Linked account not found")
    except SQLAlchemyError as error:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

# GET /linkedAccounts/{cbu}
@router.get("/{cbu}", status_code=status.HTTP_200_OK)
async def get_keys_for_linked_account(cbu: str, request: BasicAuthSchema, db: Session = Depends(get_db)):
    if not request.is_valid():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email is not valid")
    if not crud.validate_user(db, request.email, request.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    if len(cbu) != CBU_LENGTH:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "CBU length must be 22 characters")
    
    try:
        linkedAccounts = crud.get_keys_for_linked_account(cbu, db, user=request)
        if linkedAccounts:
            return linkedAccounts
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Linked account not found")
    except SQLAlchemyError as error:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)