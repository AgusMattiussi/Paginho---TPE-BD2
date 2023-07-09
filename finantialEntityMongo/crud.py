from mongoDatabase import bankAccounts_serializer, Transaction, transactions_serializer
from datetime import datetime
from decimal import Decimal

# Accounts
def get_account(cbu, collection):
    accounts = bankAccounts_serializer(collection.find({"_id": cbu}))
    return accounts

def validate_account(cbu, collection):
    return collection.count_documents({"_id": cbu}) > 0

def modify_balance(cbu, amount, collection):
    # account = db.query(BankAccount).filter(BankAccount.cbu == cbu).first()
    # account.balance += Decimal(amount)
    # db.commit()
    # db.refresh(account)
    return {"TO": "DO"}

# Transactions
def create_transaction(collection, cbuFrom: str, cbuTo: str, amount: float):
    formattedDatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _transaction = Transaction(time= formattedDatetime, cbuFrom=cbuFrom, cbuTo=cbuTo, amount=amount)

    _id = collection.insert_one(dict(_transaction))
    transaction = transactions_serializer(collection.find({"_id": _id.inserted_id}))

    # modify_balance(cbuFrom, -amount, db)
    # modify_balance(cbuTo, amount, db)

    return transaction
