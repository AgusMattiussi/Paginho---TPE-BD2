from typing import Optional
from pydantic import BaseModel

import validators

class TransactionSchema(BaseModel):
    cbuFrom: str = None
    cbuTo: str = None
    amount: str = None

    def is_valid(self):
        if not self.cbuFrom or not self.cbuTo or not self.amount:
            return False
        return  validators.validate_cbu(self.cbuFrom) and \
                validators.validate_cbu(self.cbuTo) and \
                validators.validate_amount(self.amount)

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
