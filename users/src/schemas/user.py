from pydantic import BaseModel, validator


class UserBase(BaseModel):
    email: str
    phone: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str
    password_confirmation: str
    redirect_url: str | None = None

    @validator("password_confirmation")
    def passwords_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v


class UserLogin(BaseModel):
    email: str
    password: str


class UserCreateDB(UserBase):
    hashed_password: str

    class Config:
        orm_mode = True


class UserUpdate(UserCreate):
    pass
