from datetime import datetime

from pydantic import BaseModel, validator, EmailStr

from src.enums import BustType
from src.utils import validate_phone
from src.utils.url_validation import validate_url


# Base
class UserBase(BaseModel):
    email: EmailStr | None = None
    phone: str | None = None

    class Config:
        orm_mode = True
        use_enum_values = True

    @validator("phone")
    def phone_validation(cls, v):
        return validate_phone(v)


class UserId(BaseModel):
    id: int


class UserInfo(UserBase):
    email: EmailStr | None = None
    phone: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    avatar: str | None = None
    birth_date: datetime | None = None
    uae_id: str | None = None
    passport_id: str | None = None
    street: str | None = None
    city: str | None = None
    country: str | None = None
    state: str | None = None
    instagram_url: str | None = None
    height: float | None = None
    weight: float | None = None
    bust_type: BustType | None = None


# endregion

# region Auth
class UserCreate(UserBase):
    email: EmailStr
    phone: str
    password: str
    password_confirmation: str
    redirect_url: str | None = None

    @validator("password_confirmation")
    def passwords_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v

    @validator("redirect_url")
    def redirect_url_validation(cls, v):
        return validate_url(v)


class UserLogin(BaseModel):
    email: str
    password: str


class UserCreateDB(UserBase):
    hashed_password: str


# endregion


class UserUpdate(UserInfo):
    pass


class UserResponse(UserInfo, UserId):
    pass
