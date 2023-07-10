from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pgDatabase import BankAccount, Transaction
from datetime import datetime
from decimal import Decimal
from schemas import TransactionDTO
from utils import TransactionTypes

class NotEnoughFundsException(Exception):
    """Raised when the account doesn't have enough funds to make the transaction"""
    pass

# Accounts
def get_account(cbu, db: Session):
    account = db.query(BankAccount).filter(BankAccount.cbu == cbu).first()
    return account

def validate_account(cbu, db: Session):
    return db.query(BankAccount).filter(BankAccount.cbu == cbu).count() == 1

def modify_balance(cbu, amount, db: Session):
    account = db.query(BankAccount).filter(BankAccount.cbu == cbu).first()
    account.balance += Decimal(amount)

    try:
        db.commit()
        db.refresh(account)
    except SQLAlchemyError:
        raise

    return

def validate_transaction(cbu: str, amount: float, db: Session):
    balance = db.query(BankAccount.balance).filter(BankAccount.cbu == cbu).first()[0]
    return balance >= amount

# Transactions
def create_transaction(db: Session, cbuFrom: str, cbuTo: str, amount: float, multiple_bank_transaction: int):
    if multiple_bank_transaction != TransactionTypes.ADD_FUNDS:
        if not validate_transaction(cbuFrom, amount, db):
            raise NotEnoughFundsException()

    formattedDatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _transaction = Transaction(time= formattedDatetime, cbuFrom=cbuFrom, cbuTo=cbuTo, amount=amount)
 
    try:
        match multiple_bank_transaction:
                case TransactionTypes.INTERNAL:
                    modify_balance(cbuFrom, -amount, db)
                    modify_balance(cbuTo, amount, db)
                case TransactionTypes.SUBSTRACT_FUNDS:
                    modify_balance(cbuFrom, -amount, db)
                case TransactionTypes.ADD_FUNDS:
                    modify_balance(cbuTo, amount, db) 
    except Exception:
        raise 

    try:
        db.add(_transaction)
        db.commit()
        db.refresh(_transaction)
    except SQLAlchemyError:
        raise   

    return _transaction
