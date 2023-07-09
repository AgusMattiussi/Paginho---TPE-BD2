from sqlalchemy.orm import Session
from pgDatabase import BankAccount, Transaction
from datetime import datetime
from decimal import Decimal


# Accounts
def get_account(cbu, db: Session):
    account = db.query(BankAccount).filter(BankAccount.cbu == cbu).first()
    return account

def validate_account(cbu, db: Session):
    return db.query(BankAccount).filter(BankAccount.cbu == cbu).count() > 0

def modify_balance(cbu, amount, db: Session):
    account = db.query(BankAccount).filter(BankAccount.cbu == cbu).first()
    account.balance += Decimal(amount)
    db.commit()
    db.refresh(account)
    return

# Transactions
def create_transaction(db: Session, cbuFrom: str, cbuTo: str, amount: float):
    formattedDatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _transaction = Transaction(time= formattedDatetime, cbuFrom=cbuFrom, cbuTo=cbuTo, amount=amount)
    db.add(_transaction)
    db.commit()
    db.refresh(_transaction)

    modify_balance(cbuFrom, -amount, db)
    modify_balance(cbuTo, amount, db)

    return _transaction
