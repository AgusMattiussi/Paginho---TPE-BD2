from typing import Optional
from pydantic import BaseModel

class UserSchema(BaseModel): # POST /users
    email: str = None
    name: str = None
    password: str = None
    cuit: str = None
    phoneNumber: str = None

    class Config:
        orm_mode = True


class LinkedUserSchema(BaseModel): # GET /users
    cbu: str = None

    class Config:
        orm_mode = True


class BasicAuthSchema(BaseModel):  # GET /linkedAccounts | GET /linkedAccounts/{cbu} (el cbu como es un path param se lee directamente de la url)
    email: str = None
    password: str = None

    class Config:
        orm_mode = True


class LinkedAccountsPostSchema(BaseModel): # POST /linkedAccounts
    email: str = None
    password: str = None
    cbu: str = None

    class Config:
        orm_mode = True


class LinkedAccountsPutSchema(BaseModel): # PUT /linkedAccounts/{cbu}
    email: str = None
    password: str = None
    key: str = None

    class Config:
        orm_mode = True


class TransactionsGetSchema(BaseModel): # GET /transactions
    email: str = None
    password: str = None
    limit: int = None

    class Config:
        orm_mode = True


class TransactionsPostSchema(BaseModel): # POST /transactions
    email: str = None
    password: str = None
    cbu: str = None
    key: str = None
    amount: float = None

    class Config:
        orm_mode = True


class TestSchema(BaseModel): # POST /transactions
    cbu1: str = None
    cbu2: str = None
    amount: float = None
    
    class Config:
        orm_mode = True