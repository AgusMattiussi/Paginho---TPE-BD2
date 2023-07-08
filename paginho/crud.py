from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pgDatabase import User, LinkedEntity, FinancialEntity, Transaction
from schemas import UserSchema, BasicAuthSchema, LinkedAccountsPostSchema, LinkedAccountsPutSchema
from schemas import UserSchema

from datetime import datetime

CBU_LENGTH = 22

# User
def create_user(db: Session, user: UserSchema):
    _user = User(email=user.email,
                name=user.name, 
                password=user.password, 
                cuit=user.cuit, 
                phoneNumber=user.phoneNumber)
    db.add(_user)
    db.commit()
    db.refresh(_user)
    return _user

def get_user(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def get_user_by_cbu(db: Session, cbu: str):
    return db.query(User).join(LinkedEntity).filter(LinkedEntity.cbu == cbu).first()
    

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

    # Insertar nueva tupla en LinkedEntity
    _linkedEntity = LinkedEntity(cbu=cbu, key=None, entityId=entityId, userId=userId)
    db.add(_linkedEntity)
    db.commit()
    db.refresh(_linkedEntity)
    return _linkedEntity

def modify_linked_account(cbu, db: Session, user: LinkedAccountsPutSchema):
    # Verificar validez del CBU
    if(len(cbu) != CBU_LENGTH):
        return {"Error" : "El CBU no es válido"}
    
    # Verificar que no supere el limite de vinculaciones por cuenta
    if(db.query(LinkedEntity).join(User).filter(User.email == user.email).count() > 10):
        return {"Error" : "Se superó el límite de vinculaciones para esta cuenta"}
    
    # Verificar que no supere el limite de vinculaciones por entidad financiera
    if(db.query(LinkedEntity).filter(cbu == LinkedEntity.cbu).count() > 5):
        return {"Error" : "Se superó el límite de vinculaciones para este CBU"}
    
    # Buscar el dueño del CBU en la tabla User
    owner = db.query(User).filter(User.email == user.email).first()

    # Buscar el banco asociado al CBU en la tabla FinancialEntity
    entity = db.query(FinancialEntity).filter(FinancialEntity.id == cbu[:3]).first()

    # Buscar la LinkedEntity a modificar con el CBU
    linkedEntity = db.query(LinkedEntity).filter(LinkedEntity.cbu == cbu).first()

    # Modificar la tupla en LinkedEntity segun el valor de la key (email, phone, cuit)
    if user.key == "email":
        newKey = owner.email
    elif user.key == "phone":
        newKey = owner.phoneNumber
    elif user.key == "cuit":
        newKey = owner.cuit
    else:
        newKey = user.key

    if(linkedEntity.key == None):
        linkedEntity.key = [newKey]
    else:
        linkedEntity.key.append(newKey)
    
    # Modificar la tupla
    db.query(LinkedEntity).filter(LinkedEntity.cbu == cbu).update({'key': linkedEntity.key})
    db.commit()
    return linkedEntity


# Transactions
def create_transaction(db: Session, cbuFrom: str, cbuTo: str, amount: float):
    formattedDatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _transaction = Transaction(time= formattedDatetime, cbuFrom=cbuFrom, cbuTo=cbuTo, amount=amount)
    db.add(_transaction)
    db.commit()
    db.refresh(_transaction)
    return _transaction
