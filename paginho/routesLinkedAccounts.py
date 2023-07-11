from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from pgDatabase import get_db
from sqlalchemy.orm import Session
from schemas import BasicAuthSchema, LinkedAccountsPostSchema, LinkedAccountsPutSchema, LinkedAccountDTO, LinkedAccountListDTO

import crud, redisDatabase, validators

CBU_LENGTH = 22

router = APIRouter()

# GET /linkedAccounts
@router.get("/", status_code=status.HTTP_200_OK)
async def get_linked_accounts(request: BasicAuthSchema, db: Session = Depends(get_db)):
    if not request.is_valid():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email is not valid")
    if not crud.validate_user(db, request.email, request.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")

    linkedAccounts = []
    try:
        linkedAccount = crud.get_linked_entities_by_email(db, email=request.email)
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    for account in linkedAccount:
        linkedAccounts.append(LinkedAccountDTO(cbu=account["cbu"], bank=account["name"], keys=account["keys"]))

    return LinkedAccountListDTO(linkedAccounts=linkedAccounts)

# POST /linkedAccounts
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_linked_account(request: LinkedAccountsPostSchema, db: Session = Depends(get_db)):
    if not request.is_valid():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "One or more fields is not valid")
    if not crud.validate_user(db, request.email, request.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    # Buscar el usuario en la tabla User
    user = crud.get_user_by_email(db, request.email)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    # Buscar el banco asociado al CBU en la tabla FinancialEntity
    entity = crud.get_financial_entity_from_cbu(db, request.cbu)
    if not entity:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Financial entity does not exist or is not supported")
    try:
        crud.create_linked_entity(db, email=user.email, cbu=request.cbu, userId=user.id, entityId=entity.id)
    except crud.AccountVinculationLimitException:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Account vinculation limit reached")
    except crud.CBUVinculationLimitException:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "CBU vinculation limit reached")
    except crud.CBUAlreadyVinculatedException:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "CBU already vinculated")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error")    
    return LinkedAccountDTO(cbu=request.cbu, bank=entity.name)

# PUT /linkedAccounts/{cbu}
@router.put("/{cbu}", status_code=status.HTTP_200_OK)
async def modify_linked_account(cbu: str, request: LinkedAccountsPutSchema, db: Session = Depends(get_db)):
    if not request.is_valid():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "One or more fields is not valid")
    if not crud.validate_user(db, request.email, request.password, cbu):
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
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error xd")
    linkedAccount = None
    try:
        linkedAccount = crud.modify_linked_entity(db, email=request.email, key=solvedKey, cbu=cbu)
        if linkedAccount is None:
            redisDatabase.delete_key(solvedKey)
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Linked account not found")
    except crud.AccountVinculationLimitException:
        redisDatabase.delete_key(solvedKey)
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Account vinculation limit reached")
    except crud.CBUVinculationLimitException:
        redisDatabase.delete_key(solvedKey)
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "CBU vinculation limit reached")      
    except Exception:
        redisDatabase.delete_key(solvedKey)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error")
    
    return LinkedAccountDTO(cbu=linkedAccount.cbu, bank=entity.name,  keys=linkedAccount.key)
    


# GET /linkedAccounts/{cbu}
@router.get("/{cbu}", status_code=status.HTTP_200_OK)
async def get_linked_account(cbu: str, request: BasicAuthSchema, db: Session = Depends(get_db)):
    if not request.is_valid():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email is not valid")
    if not crud.validate_user(db, request.email, request.password, cbu):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials or inexistent CBU")

    response = {}
    try:
        linkedAccount = crud.get_keys_for_linked_account(db, cbu)
        if linkedAccount:
            response = LinkedAccountDTO(cbu=linkedAccount["cbu"], bank=linkedAccount["name"], keys=linkedAccount["keys"] or [])
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error")
    return response

def _internal_delete_key(db: Session, email: str, key: str, cbu: str):
    solvedKey = crud.solve_key(db, email, key)
    if not solvedKey:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    
    entity = crud.get_financial_entity_from_cbu(db, cbu)
    if not entity:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Financial entity does not exist or is not supported")
    
    linkedAccount = None
    try:
        linkedAccount = crud.delete_key_from_linked_entity(db, solvedKey, cbu)
        if not linkedAccount:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "The key specified does not exist for this account")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error")
    
    try:
        if not redisDatabase.delete_key(solvedKey):
            crud.modify_linked_entity(db, email=email, key=solvedKey, cbu=cbu)
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error")
    
    return LinkedAccountDTO(cbu=linkedAccount.cbu, bank=entity.name,  keys=linkedAccount.key)


# DELETE /linkedAccounts/{cbu}
@router.delete("/{cbu}", status_code=status.HTTP_200_OK,)
async def delete_all_keys(cbu: str, request: BasicAuthSchema, db: Session = Depends(get_db)):
    if not request.is_valid():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email is not valid")
    if not crud.validate_user(db, request.email, request.password, cbu):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    
    linkedAccount = crud.get_linked_entity(db, cbu)
    if not linkedAccount:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Linked account not found")
    
    entity = crud.get_financial_entity_from_cbu(db, cbu)
    if not entity:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Financial entity does not exist or is not supported")
    
    try:
        if not linkedAccount.key or len(linkedAccount.key) == 0:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "No keys to delete")
        keys = linkedAccount.key.copy()
        for key in keys:
            if not _internal_delete_key(db, request.email, key, cbu):
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Could not delete all keys")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error")
    
    return LinkedAccountDTO(cbu=linkedAccount.cbu, bank=entity.name,  keys=[])

# DELETE /linkedAccounts/{cbu}/{key}
@router.delete("/{cbu}/{key}", status_code=status.HTTP_200_OK)
async def delete_key(cbu: str, key:str, request: BasicAuthSchema, db: Session = Depends(get_db)):
    if not request.is_valid():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email is not valid")
    if not crud.validate_user(db, request.email, request.password, cbu):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    if not validators.validate_key_selection(key):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Key is not valid")
    
    try:
        return _internal_delete_key(db, request.email, key, cbu)
    except HTTPException:
        raise
    except Exception:
        raise
    
        