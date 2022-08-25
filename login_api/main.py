import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from .database import db
from .schemas import Token, TokenData, User, UserCreate, UserInDB
from . import crud
"""
    TODO:
        - desabilitar usuario
"""

load_dotenv()

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

# PROGRAM

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
app = FastAPI(docs_url='/', redoc_url=None)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

# DEPENDENCIES AND UTILS FUNCTIONS

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """util para registrar usuarios"""
    return pwd_context.hash(password)

def authenticate_user(db, username: str, password: str):
    user: UserInDB = crud.get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta

    else:
        expire = datetime.utcnow() + timedelta(minutes=10)
    to_encode.update({'exp': int(expire.timestamp())})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        exp: int = payload.get('exp')
        if username is None:
            raise credentials_exception
        if exp < datetime.utcnow().timestamp():
            raise HTTPException(
                    status_code=498,
                    details='Token expired',
                    headers={'WWW-Authenticate': 'Bearer'},
                )
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user


# ENDPOINTS

@app.post('/token', response_model=Token, tags=['Get-access-token'])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Incorrect username or password',
                headers={'WWW-Authenticate': 'Bearer'},
            )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
            data={'sub': user.username}, expires_delta=access_token_expires
        )
    return {'access_token': access_token, 'token_type': 'Bearer'}

@app.post('/register', response_model=Token, status_code=201, tags=['User'])
async def create_user(newUser: UserCreate):
    if (crud.get_user(db, newUser.username)):
        raise HTTPException(status_code=400, detail='username is already register')
    
    userInDB = UserInDB(
            **newUser.dict(),
            hashed_password=get_password_hash(newUser.password)
        )
    res = crud.create_user(db, userInDB)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
            data={'sub': newUser.username}, expires_delta=access_token_expires
        )
    return {'access_token': access_token, 'token_type': 'Bearer'}
    
@app.get('/users/me/', response_model=User, tags=['User'])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
