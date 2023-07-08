from fastapi import APIRouter, HTTPException, Path, status, Depends
from pgDatabase import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from psycopg2.errors import UniqueViolation
from schemas import GetUserSchema, UserDTO, PostUserSchema
import crud

CBU_LENGTH = 22

router = APIRouter()


# GET /users
@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(request: GetUserSchema, db: Session = Depends(get_db)):
    if len(request.cbu) != CBU_LENGTH:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CBU length must be 22 characters")

    try:
        user = crud.get_user_by_cbu(db, cbu=request.cbu)
        if user:
            return UserDTO(name=user.name, cuit=user.cuit, email=user.email, telephone=user.phoneNumber)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# POST /users
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(request: PostUserSchema, db: Session = Depends(get_db)):
    try:
        user = crud.create_user(db, email=request.email, name=request.name, password=request.password, cuit=request.cuit, phoneNumber=request.phoneNumber)
        if user:
            return UserDTO(name=user.name, cuit=user.cuit, email=user.email, telephone=user.phoneNumber)
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An user with this information already exists")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

#TODO: DELETE /users?



