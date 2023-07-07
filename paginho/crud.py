from sqlalchemy.orm import Session
from models import User
from schemas import UserSchema

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