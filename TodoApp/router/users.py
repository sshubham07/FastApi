from fastapi import APIRouter, Depends, HTTPException, Path
from typing import Annotated
from sqlalchemy.orm import Session
from ..models import Todos,Users
from ..database import SessionLocal
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user
from passlib.context import CryptContext


router = APIRouter(
    prefix='/users',
    tags = ['users']
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

db_dependencies = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]
bycrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

class UserVerification(BaseModel):
    password : str
    new_password :str = Field(min_length=6)

class NumberVerification(BaseModel):
    new_number :str


@router.get('/user_info',status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency, db:db_dependencies):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()
    # if user_model is None:
    #     raise HTTPException(status_code=404, detail="User  Not found")
    #return user_model
    
    
   

@router.put('/update_password/', status_code=status.HTTP_204_NO_CONTENT)
async def update_password(user:user_dependency, db:db_dependencies, user_verification:UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User Not found")
    if not bycrypt_context.verify(user_verification.password,user_model.hashed_password):
        raise HTTPException(status_code=404, detail="Old password did not match")
    user_model.hashed_password = bycrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()

@router.put('/update_phonenumber/', status_code=status.HTTP_204_NO_CONTENT)
async def update_phonenumber(user:user_dependency, db:db_dependencies, number_verification:NumberVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User Not found")
    user_model.phone_number = number_verification.new_number
    db.add(user_model)
    db.commit()


