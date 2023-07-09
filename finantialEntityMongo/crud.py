from mongoDatabase import bankAccounts_serializer, Transaction, transactions_serializer, get_bankAccount_collection
from datetime import datetime

# Accounts
def get_account(cbu, collection):
    accounts = bankAccounts_serializer(collection.find({"_id": cbu}))
    return accounts

def validate_account(cbu, collection):
    return collection.count_documents({"_id": cbu}) > 0

def modify_balance(cbu, amount, collection):
    update_operation = {"$inc": {"balance": amount}} if amount >= 0 else {"$inc": {"balance": amount}}
    collection.update_one({"_id": cbu}, update_operation)

# Transactions
def create_transaction(collection, cbuFrom: str, cbuTo: str, amount: float):
    formattedDatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _transaction = Transaction(time= formattedDatetime, cbuFrom=cbuFrom, cbuTo=cbuTo, amount=amount)

    _id = collection.insert_one(dict(_transaction))
    transaction = transactions_serializer(collection.find({"_id": _id.inserted_id}))

    bankAccountCollection = get_bankAccount_collection()
    modify_balance(cbuFrom, amount, bankAccountCollection)
    modify_balance(cbuTo, amount, bankAccountCollection)

    return transaction
