from mongoDatabase import bankAccounts_serializer, Transaction, transactions_serializer, get_bankAccount_collection
from datetime import datetime

class NotEnoughFundsException(Exception):
    """Raised when the account doesn't have enough funds to make the transaction"""
    pass

# Accounts
def get_account(cbu, collection):
    accounts = bankAccounts_serializer(collection.find({"_id": cbu}))
    return accounts

def validate_account(cbu, collection):
    return collection.count_documents({"_id": cbu}) > 0

def modify_balance(cbu, amount, collection):
    collection.update_one({"_id": cbu}, {"$inc": {"balance": amount}})

def validate_transaction(cbu: str, amount: float, collection):
    balance = bankAccounts_serializer(collection.find({"_id": cbu}))[0]['balance']
    return balance >= amount

# Transactions
def create_transaction(collection, cbuFrom: str, cbuTo: str, amount: float, multiple_bank_transaction: int):
    bankAccountCollection = get_bankAccount_collection()

    if multiple_bank_transaction != 2:
        if not validate_transaction(cbuFrom, amount, bankAccountCollection):
            raise NotEnoughFundsException()
    
    formattedDatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _transaction = Transaction(time= formattedDatetime, cbuFrom=cbuFrom, cbuTo=cbuTo, amount=amount)

    _id = collection.insert_one(dict(_transaction))
    transaction = transactions_serializer(collection.find({"_id": _id.inserted_id}))

    match multiple_bank_transaction:
            case 0:
                modify_balance(cbuFrom, -amount, bankAccountCollection)
                modify_balance(cbuTo, amount, bankAccountCollection)
            case 1:
                modify_balance(cbuFrom, -amount, bankAccountCollection)
            case 2:
                modify_balance(cbuTo, amount, bankAccountCollection)

    return transaction
