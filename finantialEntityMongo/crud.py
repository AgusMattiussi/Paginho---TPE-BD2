from mongoDatabase import BankAccount, Transaction
from datetime import datetime
from decimal import Decimal

# Accounts
def get_account(cbu, collection):
    return collection.find_one({"_id": cbu})

# def validate_account(cbu, db):
#     return db.query(BankAccount).filter(BankAccount.cbu == cbu).count() > 0

def modify_balance(cbu, amount, collection):
    # account = db.query(BankAccount).filter(BankAccount.cbu == cbu).first()
    # account.balance += Decimal(amount)
    # db.commit()
    # db.refresh(account)
    return {"TO": "DO"}

# Transactions
def create_transaction(collection, cbuFrom: str, cbuTo: str, amount: float):
    # formattedDatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # _transaction = Transaction(time= formattedDatetime, cbuFrom=cbuFrom, cbuTo=cbuTo, amount=amount)

    # collection.insert_one(dict(_transaction))

    # # modify_balance(cbuFrom, -amount, db)
    # # modify_balance(cbuTo, amount, db)

    # return _transaction
    return {"TO": "DO"}
