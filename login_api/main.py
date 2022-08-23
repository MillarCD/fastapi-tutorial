import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field

"""
    TODO: - seperar metodos de la base de datos
          - hashear password
          - añadir usuario

          - incluir mongodb

"""


load_dotenv()

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

# PROGRAM

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

# CLASSES MODELS

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None


class UserBase(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None

class User(UserBase):
    disabled: bool | None = None

class UserCreate(UserBase):
    password: str = Field(default=..., min_length=6)

class UserInDB(User):
    hashed_password: str

# DEPENDENCIES AND UTILS FUNCTIONS

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """util para registrar usuarios"""
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta

        print(f'datetime: {datetime.utcnow().timestamp()}')
        print(f'expire: {expire.timestamp()}')
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
    user = get_user(fake_users_db, username=token_data.username)
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
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
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

@app.post('/register', response_model=UserBase, status_code=201, tags=['User'])
async def create_user(newUser: UserCreate):
    if (get_user(fake_users_db, newUser.username)):
        raise HTTPException(status_code=400, detail='username is already register')

    return newUser
    
@app.get('/users/me/', response_model=User, tags=['User'])
async def read_users_me(current_user: User = Depends(get_current_active_user)):

    return current_user

@app.get('/', tags=['General'])
async def hello():
    return {'content': 'hello world'}
