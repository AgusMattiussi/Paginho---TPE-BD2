from typing import Optional
from pydantic import BaseModel


class TransactionSchema(BaseModel):
    cbuFrom: str = None
    cbuTo: str = None
    amount: float = None

class AccountDTO(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    cuit: Optional[str] = None
    telephone: Optional[str] = None
    balance: Optional[float] = None


class TransactionDTO(BaseModel):
    timestamp: Optional[str] = None
    cbuFrom: Optional[str] = None
    cbuTo: Optional[str] = None
    amount: Optional[float] = None
