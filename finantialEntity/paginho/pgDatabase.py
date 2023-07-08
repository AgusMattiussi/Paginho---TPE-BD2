from sqlalchemy import create_engine, inspect, Column, ForeignKey, Integer, TEXT, CHAR, VARCHAR, TIMESTAMP, DECIMAL, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
from sqlalchemy.dialects.postgresql import UUID


DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOSTNAME}:{settings.DATABASE_PORT}/{settings.POSTGRES_DB}"
"""{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"""

#TODO: Eliminar echo=True
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush = False, bind=engine)
Base = declarative_base()

inspector = inspect(engine)
# Check if database's FinancialEntity table needs to be populated
shouldInsertFEInfo = not inspector.has_table('BankAccount')


class BankAccount(Base):
    __tablename__ = 'BankAccount'
    cbu = Column("CBU", CHAR(22), primary_key=True, nullable=False, unique=True)
    accountType = Column("Type", Integer, nullable=False)
    name = Column("Name", TEXT, nullable=False)
    email = Column("Email", TEXT, unique=True, nullable=False)
    password = Column("Password", TEXT, nullable=False)
    cuit = Column("CUIT", CHAR(13), unique=True, nullable=False)
    phoneNumber = Column("PhoneNumber", VARCHAR(20), unique=True, nullable=False)
    balance = Column("Balance", DECIMAL(12,2), nullable=False)

class Transaction(Base):
    __tablename__ = 'Transaction'
    time = Column("Time", TIMESTAMP, primary_key=True, nullable=False)
    cbuFrom = Column("CBU1", CHAR(22), primary_key=True, nullable=False)
    cbuTo = Column("CBU2", CHAR(22), primary_key=True, nullable=False)
    amount = Column("Amount", DECIMAL(12,2), nullable=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _populate_db():
    db = SessionLocal()
    toInsert = [] 

    toInsert.append(BankAccount(cbu="0110590940090418135201", accountType=1, name="Julian Sasso", email="jsasso@itba.edu.ar", password="pass123", cuit="20-43036619-0", phoneNumber = "+54 011 3932-3701", balance=10000.00))
    
    for i in toInsert:
        db.add(i)
        db.commit()

    
    for i in toInsert:
        db.refresh(i)


def _create_db_if_not_exists():
    Base.metadata.create_all(engine)

    if(shouldInsertFEInfo):
        _populate_db()


# Initialize DB
_create_db_if_not_exists()
    