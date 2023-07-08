from fastapi import FastAPI, Depends
from pgDatabase import get_db
from sqlalchemy.orm import Session
from schemas import TestSchema
import crud
import routesUsers, routesLinkedAccounts

app = FastAPI()

app.include_router(routesUsers.router, prefix="/users", tags=["users"])
app.include_router(routesLinkedAccounts.router, prefix="/linkedAccounts", tags=["linkedAccounts"])

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/trans")
async def create_transaction(request: TestSchema, db: Session = Depends(get_db)):
    return crud.create_transaction(db, cbuFrom=request.cbu1, cbuTo=request.cbu2, amount=request.amount)