from database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, TEXT, CHAR, Integer, Sequence, String, Boolean, text, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    id = Column("UserID", Integer, Sequence('users_UserID_seq'), primary_key=True, nullable=False)
    email = Column("Email", Text, unique=True, nullable=False)
    name = Column("Name", String,  nullable=False)
    password = Column("Password", String, nullable=False)
    cuit = Column("CUIT", String(13), nullable=False)
    phoneNumber = Column("PhoneNumber", String(20), nullable=False)