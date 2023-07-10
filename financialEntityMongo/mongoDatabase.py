from config import settings
from pymongo import MongoClient
from pydantic import BaseModel
from hash import hash_password

TRANSACTION_COLLECTION_NAME = "Transaction"
BANKACCOUNT_COLLECTION_NAME = "BankAccount"

DATABASE_URL = f"mongodb://{settings.MONGO_DB_HOSTNAME}:{settings.DATABASE_PORT}"
client = MongoClient(DATABASE_URL)
db = client.financialEntity


class BankAccount(BaseModel):
    accountType: str
    name: str
    email: str
    password: str
    cuit: str
    phoneNumber: str
    balance: float

def bankAccount_serializer(bankAccount) -> dict:
    return {
        'id':bankAccount["_id"],
        'accountType':bankAccount["accountType"],
        'name':bankAccount["name"],
        'email':bankAccount["email"],
        'password':bankAccount["password"],
        'cuit':bankAccount["cuit"],
        'phoneNumber':bankAccount["phoneNumber"],
        'balance':bankAccount["balance"]
    }

def bankAccounts_serializer(bankAccounts) -> list:
    return [bankAccount_serializer(bankAccount) for bankAccount in bankAccounts]



class Transaction(BaseModel):
    time: str
    cbuFrom: str
    cbuTo: str
    amount: str

def transaction_serializer(transaction) -> dict:
    return {
        'id':transaction["_id"],
        'time':transaction["time"],
        'cbuFrom':transaction["cbuFrom"],
        'cbuTo':transaction["cbuTo"],
        'amount':transaction["amount"]
    }

def transactions_serializer(transactions) -> list:
    return [transaction_serializer(transaction) for transaction in transactions]



def get_db():
    return db

def get_bankAccount_collection():
    return db[BANKACCOUNT_COLLECTION_NAME]

def get_transaction_collection():
    return db[TRANSACTION_COLLECTION_NAME]

def _populate_db():
    toInsert = [] 

    toInsert.append(
    {
        "_id": "0010590940090418135201",
        "accountType": "1",
        "name": "Julian Sasso",
        "email": "jsasso@itba.edu.ar",
        "password": hash_password("pass123"),
        "cuit": "20-43036619-0",
        "phoneNumber": "+54 011 3932-3701",
        "balance": 10000
    })
    toInsert.append(
    {
        "_id": "0014239328123719132482",
        "accountType": "1",
        "name": "Agustin Mattiussi",
        "email": "amattiussi@itba.edu.ar",
        "password": hash_password("pass123"),
        "cuit": "20-43084142-5",
        "phoneNumber": "+54 911 3896-0800",
        "balance": 50000
    })

    get_bankAccount_collection().insert_many(toInsert)


def _create_collections_if_not_exists():
    if not "BankAccount" in db.list_collection_names():
        db.create_collection("BankAccount")
        _populate_db()
    
    if not "Transaction" in db.list_collection_names():
        db.create_collection("Transaction")


# Initialize DB
_create_collections_if_not_exists()
