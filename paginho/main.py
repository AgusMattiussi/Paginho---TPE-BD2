from fastapi import FastAPI, Depends
from pgDatabase import get_db
from sqlalchemy.orm import Session
from schemas import TestSchema
import crud
import routesUsers, routesLinkedAccounts, routesTransactions

app = FastAPI()

app.include_router(routesUsers.router, prefix="/users", tags=["users"])
app.include_router(routesLinkedAccounts.router, prefix="/linkedAccounts", tags=["linkedAccounts"])
app.include_router(routesTransactions.router, prefix="/transactions", tags=["transactions"])

@app.get("/")
async def root():
    return {"message": "Hello World"}
