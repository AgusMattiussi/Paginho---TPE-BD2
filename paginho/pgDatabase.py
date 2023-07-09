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
shouldInsertFEInfo = not inspector.has_table('FinancialEntity')


class User(Base):
    __tablename__ = 'User'
    id = Column("UserID", Integer, primary_key=True, nullable=False, unique=True)
    email = Column("Email", TEXT, unique=True, nullable=False)
    name = Column("Name", TEXT, nullable=False)
    password = Column("Password", TEXT, nullable=False)
    cuit = Column("CUIT", CHAR(13), unique=True, nullable=False)
    phoneNumber = Column("PhoneNumber", VARCHAR(20), unique=True, nullable=False)

class FinancialEntity(Base):
    __tablename__ = 'FinancialEntity'
    id = Column("EntityID", CHAR(3), primary_key=True, nullable=False, autoincrement=False, unique=True)
    name = Column("Name", TEXT, nullable=False, unique=True)

class LinkedEntity(Base):
    __tablename__ = 'LinkedEntity'
    cbu = Column("CBU", CHAR(22), primary_key=True, nullable=False)
    key = Column("Key", ARRAY(TEXT))
    entityId = Column("EntityID", CHAR(3), ForeignKey("FinancialEntity.EntityID"), nullable=False)
    userId = Column("UserID", Integer, ForeignKey("User.UserID"), nullable=False)

class Transaction(Base):
    __tablename__ = 'Transaction'
    time = Column("Time", TIMESTAMP, primary_key=True, nullable=False)
    cbuFrom = Column("CBU1", CHAR(22), ForeignKey("LinkedEntity.CBU"), primary_key=True, nullable=False)
    cbuTo = Column("CBU2", CHAR(22), ForeignKey("LinkedEntity.CBU"), primary_key=True, nullable=False)
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

    toInsert.append(FinancialEntity(id="011", name="Banco de la Nación Argentina"))
    toInsert.append(FinancialEntity(id="014", name="Banco de la Provincia de Buenos Aires"))
    toInsert.append(FinancialEntity(id="015", name="Industrial and Commercial Bank of China S.A."))
    toInsert.append(FinancialEntity(id="017", name="BBvA Banco Francés S.A."))

    toInsert.append(User(email="jsasso@itba.edu.ar", name="Julian Sasso", password="pass123", cuit="20-43036619-0", phoneNumber = "+54 11 1234-5600"))
    
    toInsert.append(LinkedEntity(cbu="0110590940090418135201", key=["potato"], entityId="011", userId=1))

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
    