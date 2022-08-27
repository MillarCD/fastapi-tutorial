from pydantic import BaseModel, Field

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None


class UserBase(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None

class UserCreate(UserBase):
    password: str = Field(default=..., min_length=6)

class User(UserBase):
    disabled: bool = False

class UserInDB(User):
    hashed_password: str

class UserUpdatingData(BaseModel):
    email: str | None = None
    full_name: str | None = None
    disabled: bool = False

