from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pgDatabase import User, LinkedEntity, FinancialEntity, Transaction
from schemas import PostUserSchema, BasicAuthSchema, LinkedAccountsPostSchema
from psycopg2.errors import UniqueViolation
from datetime import datetime



# User 
#TODO: Validar que los campos tengan el formato correcto
def create_user(db: Session, user: PostUserSchema):
    _user = User(email=user.email,
                name=user.name, 
                password=user.password, 
                cuit=user.cuit, 
                phoneNumber=user.phoneNumber)
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

#TODO: Validar que los campos tengan el formato correcto
def get_user_by_cbu(db: Session, cbu: str):
    return db.query(User).join(LinkedEntity).filter(LinkedEntity.cbu == cbu).first()
    

# LinkedEntity
def get_linked_entities(db: Session, user: BasicAuthSchema):
    return db.query(LinkedEntity.cbu, FinancialEntity.name, LinkedEntity.key).join(User, LinkedEntity.userID == User.id).join(FinancialEntity, LinkedEntity.entityId == FinancialEntity.id).filter(User.email == user.email, User.password == user.password).all()

def create_linked_entity(db: Session, user: LinkedAccountsPostSchema):
    # Verificar que no supere el limite de vinculaciones
    if(db.query(LinkedEntity).join(User, LinkedEntity.userID == User.id).filter(User.email == user.email).count() > 4):
        return "Error: Se superó el límite de vinculaciones"

    # Buscar el dueño del CBU en la tabla User
    cbu = user.cbu
    userId = db.query(User.id).join(LinkedEntity, LinkedEntity.userID == User.id).filter(LinkedEntity.cbu == cbu).first()[0]	

    # Buscar el banco asociado al CBU en la tabla FinancialEntity
    entityId = db.query(FinancialEntity.id).join(LinkedEntity, LinkedEntity.entityId == FinancialEntity.id).filter(LinkedEntity.cbu == cbu).first()[0]
    
    # Verificar validez del CBU?

    # Insertar nueva tupla en LinkedEntity -> Key = "NO_KEY"
    _linkedEntity = LinkedEntity(cbu=cbu, key="NO_KEY", entityId=entityId, userId=userId)
    db.add(_linkedEntity)
    db.commit()
    db.refresh(_linkedEntity)
    return _linkedEntity

def modify_linked_entity(cbu, db: Session, user: LinkedAccountsPostSchema):
    # Verificar que el CBU exista en la tabla LinkedEntity
    if(db.query(LinkedEntity).filter(LinkedEntity.cbu == user.cbu).count() == 0):
        return "Error: El CBU no está vinculado"

    # Verificar que no supere el limite de vinculaciones
    if(db.query(LinkedEntity).join(User, LinkedEntity.userID == User.id).filter(User.email == user.email).count() > 4):
        return "Error: Se superó el límite de vinculaciones"

    # Verificar que el usuario no haya superado el limite de keys para ese CBU

    # Buscar el banco asociado al CBU en la tabla FinancialEntity
    
    # Verificar validez del CBU?

    # Modificar la tupla en LinkedEntity segun el valor de la key (email, phone, cuit)

    return"TO DO"



# Transactions
def create_transaction(db: Session, cbuFrom: str, cbuTo: str, amount: float):
    formattedDatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _transaction = Transaction(time= formattedDatetime, cbuFrom=cbuFrom, cbuTo=cbuTo, amount=amount)
    db.add(_transaction)
    db.commit()
    db.refresh(_transaction)
    return _transaction
