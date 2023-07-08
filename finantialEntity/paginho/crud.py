from sqlalchemy.orm import Session
from pgDatabase import BankAccount, Transaction
from datetime import datetime


# Accounts
def get_account(cbu, db: Session):
    account = db.query(BankAccount).filter(BankAccount.cbu == cbu).first()
    return account

# Transactions
def create_transaction(db: Session, cbuFrom: str, cbuTo: str, amount: float):
    formattedDatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _transaction = Transaction(time= formattedDatetime, cbuFrom=cbuFrom, cbuTo=cbuTo, amount=amount)
    db.add(_transaction)
    db.commit()
    db.refresh(_transaction)
    return _transaction
