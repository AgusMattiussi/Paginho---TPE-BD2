from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pgDatabase import User, LinkedEntity, FinancialEntity, Transaction
from schemas import PostUserSchema, BasicAuthSchema, LinkedAccountsPostSchema
from psycopg2.errors import UniqueViolation
from datetime import datetime

CBU_LENGTH = 22

# User 
#TODO: Validar que los campos tengan el formato correcto
def create_user(db: Session, email:str, name:str, password:str, cuit:str, phoneNumber:str):
    _user = User(email=email,
                name=name, 
                password=password, 
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

#TODO: Validar que los campos tengan el formato correcto
def get_user_by_cbu(db: Session, cbu: str):
    return db.query(User).join(LinkedEntity).filter(LinkedEntity.cbu == cbu).first()
    
#TODO: Hashear password
def validate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if user:
        return user.password == password
    return False


# LinkedEntity
def get_linked_entities(db: Session, user: BasicAuthSchema):
    result = db.query(LinkedEntity.cbu, FinancialEntity.name, LinkedEntity.key)\
        .join(User, LinkedEntity.userId == User.id)\
            .join(FinancialEntity, LinkedEntity.entityId == FinancialEntity.id)\
                .filter(User.email == user.email, User.password == user.password).all()
    results = []
    for row in result:
        entity_dict = {
            "cbu": row[0],
            "name": row[1],
            "key": row[2]
        }
        results.append(entity_dict)

    return results

def create_linked_entity(db: Session, user: LinkedAccountsPostSchema):
    # Verificar validez del CBU
    if(len(user.cbu) != CBU_LENGTH):
        return {"Error" : "El CBU no es válido"}

    # Verificar que no supere el limite de vinculaciones por cuenta
    if(db.query(LinkedEntity).join(User).filter(User.email == user.email).count() > 10):
        return {"Error" : "Se superó el límite de vinculaciones para esta cuenta"}
    
    # Verificar que no supere el limite de vinculaciones por entidad financiera
    if(db.query(LinkedEntity).filter(user.cbu == LinkedEntity.cbu).count() > 5):
        return {"Error" : "Se superó el límite de vinculaciones para este CBU"}

    # Buscar el dueño del CBU en la tabla User
    cbu = user.cbu
    userId = db.query(User.id).filter(User.email == user.email).first()[0]	

    # Buscar el banco asociado al CBU en la tabla FinancialEntity
    entityId = db.query(FinancialEntity.id).filter(FinancialEntity.id == cbu[:3]).first()[0]

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
