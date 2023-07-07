from database import Base, engine
from sqlalchemy import Column, ForeignKey, Integer, TEXT, CHAR, TIMESTAMP, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = 'User'
    id = Column("UserID", Integer, primary_key=True, nullable=False, unique=True)
    email = Column("Email", TEXT, unique=True, nullable=False)
    name = Column("Name", TEXT, nullable=False)
    password = Column("Password", TEXT, nullable=False)
    cuit = Column("CUIT", CHAR(13), unique=True, nullable=False)
    phoneNumber = Column("PhoneNumber", CHAR(20), unique=True, nullable=False)

class FinancialEntity(Base):
    __tablename__ = 'FinancialEntity'
    id = Column("EntityID", Integer, primary_key=True, nullable=False, autoincrement=False, unique=True)
    name = Column("Name", TEXT, nullable=False, unique=True)

class LinkedEntity(Base):
    __tablename__ = 'LinkedEntity'
    cbu = Column("CBU", CHAR(22), primary_key=True, nullable=False, unique=True)
    key = Column("Key", TEXT, primary_key=True, nullable=False)
    entityId = Column("EntityID", Integer, ForeignKey("FinancialEntity.EntityID"), nullable=False)
    userID = Column("UserID", Integer, ForeignKey("User.UserID"), nullable=False)

class Transaction(Base):
    __tablename__ = 'Transaction'
    time = Column("Time", TIMESTAMP, primary_key=True, nullable=False)
    cbuFrom = Column("CBU1", CHAR(22), ForeignKey("LinkedEntity.CBU"), primary_key=True, nullable=False)
    cbuTo = Column("CBU2", CHAR(22), ForeignKey("LinkedEntity.CBU"), primary_key=True, nullable=False)
    amount = Column("UserID", DECIMAL(12,2), nullable=False)


Base.metadata.create_all(engine)