from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pgDatabase import User, LinkedEntity, FinancialEntity, Transaction
from psycopg2.errors import UniqueViolation
from datetime import datetime
from typing import Optional
from hash import hash_password, is_valid

CBU_LENGTH = 22
ACCOUNT_VINCULATION_LIMIT = 10
FINANCIAL_ENTITY_VINCULATION_LIMIT = 5

class AccountVinculationLimitException(Exception):
    """Raised when the account vinculation limit is reached"""
    pass

class CBUVinculationLimitException(Exception):
    """Raised when the CBU vinculation limit is reached"""
    pass

class InexistentFinancialEntityException(Exception):
    """Raised when the financial entity doesn't exist"""
    pass

class CBUAlreadyVinculatedException(Exception):
    """Raised when the CBU is already vinculated"""
    pass

def _account_vinculation_count(db: Session, email: str):
    return db.query(LinkedEntity).join(User).filter(User.email == email).count()

def _cbu_vinculation_count(db: Session, cbu: str):
    keys = db.query(LinkedEntity.key).filter(LinkedEntity.cbu == cbu).first()
    if not keys or not keys[0]:
        return 0
    return len(keys[0])

# Los 3 primeros digitos del CBU identifican a la entidad financiera
def get_financial_entity_from_cbu(db: Session, cbu: str):
    return db.query(FinancialEntity).filter(FinancialEntity.id == cbu[:3]).first()

def _get_linked_entity(db: Session, cbu: str):
    return db.query(LinkedEntity).filter(LinkedEntity.cbu == cbu).first()

# User 
def create_user(db: Session, email:str, name:str, password:str, cuit:str, phoneNumber:str):
    _user = User(email=email,
                name=name, 
                password=hash_password(password), 
                cuit=cuit, 
                phoneNumber=phoneNumber)
    try:
        db.add(_user)
        db.commit()
        db.refresh(_user)
    except IntegrityError as error:
        raise error
    except SQLAlchemyError as error:
        raise error
    return _user

def get_user(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_cbu(db: Session, cbu: str):
    return db.query(User).join(LinkedEntity).filter(LinkedEntity.cbu == cbu).first()
    
def validate_user(db: Session, email: str, password: str, cbu: Optional[str] = None):
    user: None

    if cbu:
        user = db.query(User).join(LinkedEntity) \
        .filter((LinkedEntity.cbu == cbu) & (User.email == email)).first()
        # if user and user.email != email:
        #     return False
    else:
        user = db.query(User).filter(User.email == email).first()
    
    if user:
        return is_valid(password, user.password)
    return False


# LinkedEntity
def get_linked_entities_by_email(db: Session, email:str):
    result = db.query(LinkedEntity.cbu, FinancialEntity.name, LinkedEntity.key) \
                .join(User, LinkedEntity.userId == User.id) \
                .join(FinancialEntity, LinkedEntity.entityId == FinancialEntity.id) \
                .filter(User.email == email).all()
    out = []
    for row in result:
        entity_dict = {
            "cbu": row[0],
            "name": row[1],
            "keys": row[2]
        }
        out.append(entity_dict)

    return out

def create_linked_entity(db: Session, email:str, cbu:str, userId:str, entityId:str):
    # Verificar que no supere el limite de vinculaciones por cuenta
    if(_account_vinculation_count(db, email) >= ACCOUNT_VINCULATION_LIMIT):
        raise AccountVinculationLimitException()
    
    # Verificar que no supere el limite de vinculaciones por entidad financiera
    if(_cbu_vinculation_count(db, cbu) >= FINANCIAL_ENTITY_VINCULATION_LIMIT):
        raise CBUVinculationLimitException()

    # Insertar nueva tupla en LinkedEntity
    _linkedEntity = LinkedEntity(cbu=cbu, key=None, entityId=entityId, userId=userId)

    try:
        db.add(_linkedEntity)
        db.commit()
        db.refresh(_linkedEntity)
    except UniqueViolation as error:
        raise CBUAlreadyVinculatedException()
    except IntegrityError as error:
        raise CBUAlreadyVinculatedException()
    except SQLAlchemyError as error:
        raise error
    
    return _linkedEntity    



def modify_linked_entity(db: Session, email: str, key:str, cbu:str):  
    # Verificar que no supere el limite de vinculaciones por cuenta
    if(_account_vinculation_count(db, email) >= ACCOUNT_VINCULATION_LIMIT):
        raise AccountVinculationLimitException()
    
    # Verificar que no supere el limite de vinculaciones por entidad financiera
    if(_cbu_vinculation_count(db, cbu) >= FINANCIAL_ENTITY_VINCULATION_LIMIT):
        raise CBUVinculationLimitException()
    
    # Buscar la LinkedEntity a modificar con el CBU
    linkedEntity = _get_linked_entity(db, cbu)
    if not linkedEntity:
        return None

    # Agregar la key a la lista
    if(linkedEntity.key == None):
        linkedEntity.key = [key]
    else:
        linkedEntity.key.append(key)
    
    # Actualizar la tupla
    try:
        db.query(LinkedEntity).filter(LinkedEntity.cbu == cbu).update({'key': linkedEntity.key})
        db.commit()
    except SQLAlchemyError as error:
        raise error
    
    return linkedEntity

def get_keys_for_linked_account(db: Session, cbu:str):  
    result = db.query(FinancialEntity.name, LinkedEntity.key) \
                .join(FinancialEntity) \
                .filter(LinkedEntity.cbu == cbu, FinancialEntity.id == cbu[:3]).first()
    
    if result:
        return {"cbu": cbu, "name": result[0], "keys": result[1]}
    return None

# Transactions
def create_transaction(db: Session, cbuFrom: str, cbuTo: str, amount: float):
    formattedDatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _transaction = Transaction(time= formattedDatetime, cbuFrom=cbuFrom, cbuTo=cbuTo, amount=amount)

    try:
        db.add(_transaction)
        db.commit()
        db.refresh(_transaction)
    except SQLAlchemyError as e:
        raise
    return _transaction

def get_transactions_by_email(db: Session, email: str, limit: int):
    return db.query(Transaction) \
            .join(LinkedEntity, (Transaction.cbuFrom == LinkedEntity.cbu) | (Transaction.cbuTo == LinkedEntity.cbu)) \
            .join(User, (LinkedEntity.userId == User.id) & (User.email == email)) \
            .limit(limit) \
            .distinct() \
            .all()


def solve_key(db:Session, email:str, key:str):
    if(key == "email" or key == "phone" or key == "cuit"):
        owner = db.query(User).filter(User.email == email).first()
        if not owner:
            return None
        match key:
            case "email":
                return owner.email
            case "phone":
                return owner.phoneNumber
            case "cuit":
                return owner.cuit
    return key