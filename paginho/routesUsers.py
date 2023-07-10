from fastapi import APIRouter, HTTPException, status, Depends
from pgDatabase import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import GetUserSchema, UserDTO, PostUserSchema
from utils import normalizePhoneNumber

import crud

CBU_LENGTH = 22

router = APIRouter()


# GET /users
@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(request: GetUserSchema, db: Session = Depends(get_db)):
    if not request.is_valid():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "CBU is not valid")

    try:
        user = crud.get_user_by_cbu(db, cbu=request.cbu)
        if user:
            return UserDTO(name=user.name, cuit=user.cuit, email=user.email, telephone=user.phoneNumber)
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    except SQLAlchemyError as error:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)


# POST /users
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(request: PostUserSchema, db: Session = Depends(get_db)):
    if not request.is_valid():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "One or more fields is not valid")
    formattedPhoneNumber = normalizePhoneNumber(request.phoneNumber)
    
    try:
        user = crud.create_user(db, email=request.email, name=request.name, password=request.password, cuit=request.cuit, phoneNumber=formattedPhoneNumber)
        if user:
            return UserDTO(name=user.name, cuit=user.cuit, email=user.email, telephone=user.phoneNumber)
    except IntegrityError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "An user with this information already exists")
    raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)




