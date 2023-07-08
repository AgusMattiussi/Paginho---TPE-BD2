from typing import Optional
from pydantic import BaseModel

class PostUserSchema(BaseModel): # POST /users
    email: str = None
    name: str = None
    password: str = None
    cuit: str = None
    phoneNumber: str = None

    class Config:
        orm_mode = True

class GetUserSchema(BaseModel):
    cbu: str = None

    class Config:
        orm_mode = True

class UserDTO(BaseModel): # POST /users
    email: Optional[str] = None
    name: Optional[str] = None
    cuit: Optional[str] = None
    telephone: Optional[str] = None

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


class GetTransactionSchema(BaseModel): # GET /transactions
    email: str = None
    password: str = None
    limit: int = 10

    class Config:
        orm_mode = True


class PostTransactionSchema(BaseModel): # POST /transactions
    email: str = None
    password: str = None
    cbu: str = None
    key: str = None
    amount: float = None
    
    class Config:
        orm_mode = True

