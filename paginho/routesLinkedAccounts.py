from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from pgDatabase import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import BasicAuthSchema, LinkedAccountsPostSchema, LinkedAccountsPutSchema, LinkedAccountDTO
import crud, redisDatabase

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
# FIXME: CBU?
@router.put("/{cbu}", status_code=status.HTTP_200_OK)
async def modify_linked_account(cbu: str, request: LinkedAccountsPutSchema, db: Session = Depends(get_db)):
    if not request.is_valid():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "One or more fields is not valid")
    if not crud.validate_user(db, request.email, request.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    
    solvedKey = crud.solve_key(db, request.email, request.key)
    if not solvedKey:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    
    # Buscar el banco asociado al CBU en la tabla FinancialEntity
    entity = crud.get_financial_entity_from_cbu(db, cbu)
    if not entity:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Financial entity does not exist or is not supported")

    # Primero, se verifica que la key no exista en redis
    try: 
        if not redisDatabase.set_cbu(solvedKey, cbu):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Key is already in use")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    linkedAccount = None
    try:
        linkedAccount = crud.modify_linked_entity(db, email=request.email, key=solvedKey, cbu=cbu)
        if not linkedAccount:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Linked account not found")
    except crud.AccountVinculationLimitException:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Account vinculation limit reached")
    except crud.CBUVinculationLimitException:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "CBU vinculation limit reached")        
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    #TODO: Finally, delete key from redis
    
    return LinkedAccountDTO(cbu=linkedAccount.cbu, bank=entity.name,  keys=linkedAccount.keys)
    


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
    except Exception as error:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

#TODO: Delete key?