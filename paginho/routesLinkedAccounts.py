from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from pgDatabase import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import BasicAuthSchema, LinkedAccountsPostSchema, LinkedAccountsPutSchema, LinkedAccountDTO, LinkedAccountListDTO
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
    
    # Buscar el dueño del CBU en la tabla User
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
    except Exception as error:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, error._message())    
    
    return LinkedAccountDTO(cbu=request.cbu, bank=entity.name)

# PUT /linkedAccounts/{cbu}
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
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return LinkedAccountDTO(cbu=linkedAccount.cbu, bank=entity.name,  keys=linkedAccount.key)
    


# GET /linkedAccounts/{cbu}
@router.get("/{cbu}", status_code=status.HTTP_200_OK)
async def get_linked_account(cbu: str, request: BasicAuthSchema, db: Session = Depends(get_db)):
    if not request.is_valid():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email is not valid")
    if not crud.validate_user(db, request.email, request.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")

    response = {}
    try:
        linkedAccount = crud.get_keys_for_linked_account(db, cbu)
        if linkedAccount:
            response = LinkedAccountDTO(cbu=linkedAccount["cbu"], bank=linkedAccount["name"], keys=linkedAccount["keys"])
    except Exception as error:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response
#TODO: Delete key?