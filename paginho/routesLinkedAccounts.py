from fastapi import APIRouter
from fastapi import Depends
from pgDatabase import get_db
from sqlalchemy.orm import Session
from schemas import BasicAuthSchema, LinkedAccountsPostSchema, LinkedAccountsPutSchema

import crud

router = APIRouter()

# GET /linkedAccounts
@router.get("/")
async def get_linked_accounts(request: BasicAuthSchema, db: Session = Depends(get_db)):
    return crud.get_linked_entities(db, user=request)

# POST /linkedAccounts
@router.post("/")
async def create_linked_account(request: LinkedAccountsPostSchema, db: Session = Depends(get_db)):
    return crud.create_linked_entity(db, user=request)

# PUT /linkedAccounts/{cbu}
@router.put("/{cbu}")
async def modify_linked_account(cbu: str, request: LinkedAccountsPutSchema, db: Session = Depends(get_db)):
    return crud.modify_linked_entity(cbu, db, user=request)

# GET /linkedAccounts/{cbu}
# TODO:
@router.get("/{CBU}")
async def get_linked_account(request: BasicAuthSchema, db: Session = Depends(get_db)):
    return {"message" : "To be implemented"}