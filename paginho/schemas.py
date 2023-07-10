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
        if not self.email or not self.name or not self.password or not self.cuit or not self.phoneNumber:
            return False
        return  validators.validate_email(self.email) and \
                validators.validate_password(self.password) and \
                validators.validate_name(self.name) and \
                validators.validate_cuit(self.cuit) and \
                validators.validate_phone_number(self.phoneNumber)

    class Config:
        orm_mode = True

class GetUserSchema(BaseModel):
    cbu: str = None

    def is_valid(self):
        if not self.cbu:
            return False
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
        if not self.cbu:
            return False
        return validators.validate_cbu(self.cbu)

    class Config:
        orm_mode = True


class BasicAuthSchema(BaseModel):  # GET /linkedAccounts | GET /linkedAccounts/{cbu} (el cbu como es un path param se lee directamente de la url)
    email: str = None
    password: str = None

    def is_valid(self):
        if not self.email or not self.password:
            return False
        return validators.validate_email(self.email) and \
                validators.validate_password(self.password)

    class Config:
        orm_mode = True


class LinkedAccountsPostSchema(BaseModel): # POST /linkedAccounts
    email: str = None
    password: str = None
    cbu: str = None

    def is_valid(self):
        if not self.email or not self.password or not self.cbu:
            return False
        return  validators.validate_email(self.email) and \
                validators.validate_password(self.password) and \
                validators.validate_cbu(self.cbu)

    class Config:
        orm_mode = True


class LinkedAccountsPutSchema(BaseModel): # PUT /linkedAccounts/{cbu}
    email: str = None
    password: str = None
    key: str = None
    
    def is_valid(self):
        if not self.email or not self.password or not self.key:
            return False
        return  validators.validate_email(self.email) and \
                validators.validate_key_selection(self.key) and \
                validators.validate_password(self.password)

    class Config:
        orm_mode = True


class LinkedAccountDTO(BaseModel): 
    cbu: Optional[str] = None
    bank: Optional[str] = None
    keys: Optional[List[str]] = []

    class Config:
        orm_mode = True

class LinkedAccountListDTO(BaseModel): 
    linkedAccounts: Optional[List[LinkedAccountDTO]] = []
    
    class Config:
        orm_mode = True

class GetTransactionSchema(BaseModel): # GET /transactions
    email: str = None
    password: str = None
    limit: int = 10

    def is_valid(self):
        if not self.email or not self.password:
            return False
        return self.limit > 0 and \
            validators.validate_email(self.email) and \
            validators.validate_password(self.password)

    class Config:
        orm_mode = True


class PostTransactionSchema(BaseModel): # POST /transactions
    email: str = None
    password: str = None
    cbu: str = None
    key: str = None
    amount: str = None

    def is_valid(self):
        if not self.email or not self.password or not self.cbu or not self.key or not self.amount:
            return False
        return  validators.validate_email(self.email) and \
                validators.validate_password(self.password) and \
                validators.validate_cbu(self.cbu) and \
                validators.validate_alias_key(self.key) and \
                validators.validate_amount(self.amount)
    
    class Config:
        orm_mode = True

class TransactionDTO(BaseModel):
    cbuFrom: str = None
    cbuTo: str = None
    amount: float = None
    date: str = None

    class Config:
        orm_mode = True

class TransactionListDTO(BaseModel):
    transactions: Optional[List[TransactionDTO]] = []
    
    class Config:
        orm_mode = True