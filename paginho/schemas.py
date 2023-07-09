from typing import Optional, List
from pydantic import BaseModel
import validators

class PostUserSchema(BaseModel): # POST /users
    email: str = None
    name: str = None
    password: str = None
    cuit: str = None
    phoneNumber: str = None

    def is_valid(self):
        return  validators.validate_email(self.email) and \
                validators.validate_cuit(self.cuit) and \
                validators.validate_phone_number(self.phoneNumber)

    class Config:
        orm_mode = True

class GetUserSchema(BaseModel):
    cbu: str = None

    def is_valid(self):
        return validators.validate_cbu(self.cbu)

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

    def is_valid(self):
        return validators.validate_cbu(self.cbu)

    class Config:
        orm_mode = True


class BasicAuthSchema(BaseModel):  # GET /linkedAccounts | GET /linkedAccounts/{cbu} (el cbu como es un path param se lee directamente de la url)
    email: str = None
    password: str = None

    def is_valid(self):
        return validators.validate_email(self.email)

    class Config:
        orm_mode = True


class LinkedAccountsPostSchema(BaseModel): # POST /linkedAccounts
    email: str = None
    password: str = None
    cbu: str = None

    def is_valid(self):
        return  validators.validate_email(self.email) and \
                validators.validate_cbu(self.cbu)

    class Config:
        orm_mode = True


class LinkedAccountsPutSchema(BaseModel): # PUT /linkedAccounts/{cbu}
    email: str = None
    password: str = None
    key: str = None
    
    def is_valid(self):
        return  validators.validate_email(self.email) and \
                validators.validate_key_selection(self.key)

    class Config:
        orm_mode = True


class LinkedAccountDTO(BaseModel): 
    cbu: Optional[str] = None
    bank: Optional[str] = None
    keys: Optional[List[str]] = []

    class Config:
        orm_mode = True

class GetTransactionSchema(BaseModel): # GET /transactions
    email: str = None
    password: str = None
    limit: int = 10

    def is_valid(self):
        return validators.validate_email(self.email)

    class Config:
        orm_mode = True


class PostTransactionSchema(BaseModel): # POST /transactions
    email: str = None
    password: str = None
    cbu: str = None
    key: str = None
    amount: float = None

    def is_valid(self):
        return  validators.validate_email(self.email) and \
                validators.validate_cbu(self.cbu) and \
                validators.validate_alias_key(self.key) and \
                validators.validate_amount(self.amount)
    
    class Config:
        orm_mode = True

