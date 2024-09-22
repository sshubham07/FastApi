from fastapi import APIRouter, Depends,HTTPException, Request
from pydantic import BaseModel
from ..models import Users
from passlib.context import CryptContext
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt,JWSError
from datetime import timedelta,datetime,timezone
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)
bycrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')
SECRET_KEY = '3d2b1f4d6e22a44c8b75e6ffcc2f9b649ec1f0dfb9e81c4f5e3d8a82cbe576cd'
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
ALGORITHM = 'HS256'

class CreateUserRequest(BaseModel):
    username:str
    email:str
    first_name:str
    last_name:str
    password:str
    role:str
    phone_number:str

class Token(BaseModel):
    access_token:str
    token_type:str

def authenticate_user(username:str,password:str,db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bycrypt_context.verify(password, user.hashed_password):
        return False
    return user

async def get_current_user(token: Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username:str = payload.get('sub')
        user_id:int = payload.get('id')
        user_role:str = payload.get('role')
        if username is None or user_id is None or user_role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not velidate user')
        return {'username':username, 'id':user_id, 'user_role':user_role}
    except JWSError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not velidate user')

def create_access_token(user_name:str,user_id:int, role:str, expires_delta:timedelta):
    encode = {'sub':user_name, 'id':user_id,'role':role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm= ALGORITHM)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

db_dependencies = Annotated[Session, Depends(get_db)]
templates = Jinja2Templates(directory='TodoApp/templates')

### Pages
@router.get('/login-page')
def render_login_page(request:Request):
    return templates.TemplateResponse('login.html',{"request":request})

@router.get('/register-page')
def render_register_page(request:Request):
    return templates.TemplateResponse('register.html',{"request":request})
###End-Points
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db : db_dependencies, create_user_request: CreateUserRequest):
    print("Create user called")
    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        hashed_password = bycrypt_context.hash(create_user_request.password),
        role = create_user_request.role,
        is_active = True,
        phone_number = create_user_request.phone_number
    )
    db.add(create_user_model)
    db.commit()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()], db:db_dependencies):
    user = authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not velidate user')
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {'access_token':token,'token_type':'bearer'}
