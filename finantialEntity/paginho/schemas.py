from typing import Optional
from pydantic import BaseModel


class TransactionSchema(BaseModel): # POST /transactions
    cbu_from: str = None
    cbu_to: str = None
    amount: float = None
    
    class Config:
        orm_mode = True

class AccountDTO(BaseModel): # POST /users
    email: Optional[str] = None
    name: Optional[str] = None
    cuit: Optional[str] = None
    telephone: Optional[str] = None
    balance: Optional[float] = None

    class Config:
        orm_mode = True