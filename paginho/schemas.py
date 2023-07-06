from typing import Optional
from pydantic import BaseModel

class UserSchema(BaseModel):
    email: str = None
    name: str = None
    password: str = None
    cuit: str = None
    phoneNumber: str = None

    class Config:
        orm_mode = True