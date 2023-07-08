from fastapi import APIRouter
from fastapi import Depends
from pgDatabase import get_db
from sqlalchemy.orm import Session
from schemas import BasicAuthSchema, LinkedAccountsPostSchema, LinkedAccountsPutSchema

import crud

router = APIRouter()

# GET /linkedAccounts
# POST /linkedAccounts
# PUT /linkedAccounts/{cbu}
# GET /linkedAccounts/{cbu}

@router.get("/")
async def get_linked_accounts(request: BasicAuthSchema, db: Session = Depends(get_db)):
    return crud.get_linked_entities(db, user=request)

@router.post("/")
async def create_linked_account(request: LinkedAccountsPostSchema, db: Session = Depends(get_db)):
    return crud.create_linked_entity(db, user=request)

@router.put("/{cbu}")
async def modify_linked_account(cbu: str, request: LinkedAccountsPutSchema, db: Session = Depends(get_db)):
    return crud.modify_linked_entity(cbu, db, user=request)