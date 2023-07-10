from sqlalchemy.orm import Session
from pgDatabase import BankAccount, Transaction
from datetime import datetime
from decimal import Decimal

class NotEnoughFundsException(Exception):
    """Raised when the account doesn't have enough funds to make the transaction"""
    pass

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

def validate_transaction(cbu: str, amount: float, db: Session):
    balance = db.query(BankAccount.balance).filter(BankAccount.cbu == cbu).first()[0]
    return balance >= amount

# Transactions
def create_transaction(db: Session, cbuFrom: str, cbuTo: str, amount: float, multiple_bank_transaction: int):
    if multiple_bank_transaction != 2:
        if not validate_transaction(cbuFrom, amount, db):
            raise NotEnoughFundsException()

    formattedDatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _transaction = Transaction(time= formattedDatetime, cbuFrom=cbuFrom, cbuTo=cbuTo, amount=amount)
    db.add(_transaction)
    db.commit()
    db.refresh(_transaction)

    match multiple_bank_transaction:
            case 0:
                modify_balance(cbuFrom, -amount, db)
                modify_balance(cbuTo, amount, db)
            case 1:
                modify_balance(cbuFrom, -amount, db)
            case 2:
                modify_balance(cbuTo, amount, db)    

    return _transaction
