from sqlalchemy import create_engine, inspect, Column, ForeignKey, Integer, TEXT, CHAR, VARCHAR, TIMESTAMP, DECIMAL, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
from hash import hash_password

DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOSTNAME}:{settings.DATABASE_PORT}/{settings.POSTGRES_DB}"
"""{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"""

FINANCIAL_ENTITIES = {
    "000": "PostgreSQL Bank S.A.",
    "001": "MongoDB Bank S.A.",
    "005": "The Royal Bank of Scotland N.V.",
    "007": "Banco de Galicia y Buenos Aires S.A.",
    "011": "Banco de la Nación Argentina",
    "014": "Banco de la Provincia de Buenos Aires",
    "015": "Industrial and Commercial Bank of China S.A.",
    "016": "Citibank N.A.",
    "017": "BBVA Banco Francés S.A.",
    "018": "The Bank of Tokyo-Mitsubishi UFJ, LTD.",
    "020": "Banco de la Provincia de Córdoba S.A.",
    "027": "Banco Supervielle S.A.",
    "029": "Banco de la Ciudad de Buenos Aires",
    "030": "Central de la República Argentina",
    "034": "Banco Patagonia S.A.",
    "044": "Banco Hipotecario S.A.",
    "045": "Banco de San Juan S.A.",
    "046": "Banco do Brasil S.A.",
    "060": "Banco de Tucumán S.A.",
    "065": "Banco Municipal de Rosario",
    "072": "Banco Santander Río S.A.",
    "083": "Banco del Chubut S.A.",
    "086": "Banco de Santa Cruz S.A.",
    "093": "Banco de la Pampa Sociedad de Economía Mixta",
    "094": "Banco de Corrientes S.A.",
    "097": "Banco Provincia del Neuquén S.A.",
    "143": "Brubank S.A.U.",
    "147": "Banco Interfinanzas S.A.",
    "150": "HSBC Bank Argentina S.A.",
    "158": "Openbank",
    "165": "JP Morgan Chase Bank NA (Sucursal Buenos Aires)",
    "191": "Banco Credicoop Cooperativo Limitado",
    "198": "Banco de Valores S.A.",
    "247": "Banco Roela S.A.",
    "254": "Banco Mariva S.A.",
    "259": "Banco Itaú Argentina S.A.",
    "262": "Bank of America National Association",
    "266": "BNP Paribas",
    "268": "Banco Provincia de Tierra del Fuego",
    "269": "Banco de la República Oriental del Uruguay",
    "277": "Banco Sáenz S.A.",
    "281": "Banco Meridian S.A.",
    "285": "Banco Macro S.A.",
    "295": "American Express Bank LTD. S.A.",
    "299": "Banco Comafi S.A.",
    "300": "Banco de Inversión y Comercio Exterior S.A.",
    "301": "Banco Piano S.A.",
    "305": "Banco Julio S.A.",
    "309": "Nuevo Banco de la Rioja S.A.",
    "310": "Banco del Sol S.A.",
    "311": "Nuevo Banco del Chaco S.A.",
    "312": "MBA Lazard Banco de Inversiones S.A.",
    "315": "Banco de Formosa S.A.",
    "319": "Banco CMF S.A.",
    "321": "Banco de Santiago del Estero S.A.",
    "322": "Banco Industrial S.A.",
    "325": "Deutsche Bank S.A.",
    "330": "Nuevo Banco de Santa Fe S.A.",
    "331": "Banco Cetelem Argentina S.A.",
    "332": "Banco de Servicios Financieros S.A.",
    "336": "Banco Bradesco Argentina S.A.",
    "338": "Banco de Servicios y Transacciones S.A.",
    "339": "RCI Banque S.A.",
    "340": "BACS Banco de Crédito y Securitización S.A.",
    "341": "Más Ventas S.A.",
    "384": "Wilobank S.A.",
    "386": "Nuevo Banco de Entre Ríos S.A.",
    "389": "Banco Columbia S.A.",
    "405": "Ford Credit Compañía Financiera S.A.",
    "406": "Metrópolis Compañía Financiera S.A.",
    "408": "Compañía Financiera Argentina S.A.",
    "413": "Montemar Compañía Financiera S.A.",
    "415": "Transatlántica Compañía Financiera S.A.",
    "428": "Caja de Crédito Coop. La Capital del Plata LTDA.",
    "431": "Banco Coinag S.A.",
    "432": "Banco de Comercio S.A.",
    "434": "Caja de Crédito Cuenca Coop. LTDA.",
    "437": "Volkswagen Credit Compañía Financiera S.A.",
    "438": "Cordial Compañía Financiera S.A.",
    "440": "Fiat Crédito Compañía Financiera S.A.",
    "441": "GPAT Compañía Financiera S.A.",
    "442": "Mercedes-Benz Compañía Financiera Argentina S.A.",
    "443": "Rombo Compañía Financiera S.A.",
    "444": "John Deere Credit Compañía Financiera S.A.",
    "445": "PSA Finance Argentina Compañía Financiera S.A.",
    "446": "Toyota Compañía Financiera de Argentina S.A.",
    "448": "Finandino Compañía Financiera S.A.",
    "453": "Naranja X",
    "992": "Provincanje S.A."
}

engine = create_engine(DATABASE_URL, echo=False)
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
    cuit = Column("CUIT", VARCHAR(13), unique=True, nullable=False)
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
    
    for key, value in FINANCIAL_ENTITIES.items():
        toInsert.append(FinancialEntity(id=key, name=value))

    toInsert.append(User(email="jsasso@itba.edu.ar", name="Julian Sasso", password=hash_password("pass123"), cuit="20-43036619-0", phoneNumber = "+54 11 1234-5600"))
    
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
    