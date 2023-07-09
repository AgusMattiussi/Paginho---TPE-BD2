from config import settings
from pymongo import MongoClient
from pydantic import BaseModel

DATABASE_URL = f"mongodb://{settings.MONGO_DB_HOSTNAME}:{settings.DATABASE_PORT}"
client = MongoClient(DATABASE_URL)

db = client[settings.MONGO_DB_DBNAME]


class BankAccount(BaseModel):
    cbu: str
    accountType: str
    name: str
    email: str
    password: str
    cuit: str
    phoneNumber: str
    balance: float

class Transaction(BaseModel):
    __tablename__ = 'Transaction'
    time: str
    cbuFrom: str
    cbuTo: str
    amount: str


def get_db():
    return "TO DO"



def _populate_db():
    toInsert = [] 

    toInsert.append(BankAccount(cbu="0110590940090418135201", accountType=1, name="Julian Sasso", email="jsasso@itba.edu.ar", password="pass123", cuit="20-43036619-0", phoneNumber = "+54 011 3932-3701", balance=10000.00))
    toInsert.append(BankAccount(cbu="0114239328123719132482", accountType=1, name="Agustin Mattiussi", email="amattiussi@itba.edu.ar", password="pass123", cuit="20-43084142-5", phoneNumber = "+54 911 3896-0800", balance=50000.00))
    
    db.BankAccount.insert_many(toInsert)


def _create_collections_if_not_exists():
    if not "BankAccount" in db.list_collection_names():
        db.create_collection("BankAccount")
        _populate_db()
    
    if not "Transaction" in db.list_collection_names():
        db.create_collection("Transaction")


# Initialize DB
_create_collections_if_not_exists()
