from functools import partial

from fastapi import HTTPException

from src.core.base_service import BaseService, ModelType
from src.core.security import get_password_hash, verify_password
from src.models import User
from src.schemas import UserCreate, UserCreateDB, UserUpdate


class UserService(BaseService[User, UserCreate, UserUpdate]):
    def email_exists(self, email: str):
        return self.db.query(self.model).filter(self.model.email == email).first()

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def authenticate(self, email: str, password: str) -> User | None:
        user = self.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def create(self, obj_in: UserCreate) -> ModelType:
        if self.email_exists(obj_in.email):
            raise HTTPException(
                status_code=400, detail="Пользователь с данным емайлом уже зарегистрирован"
            )
        hashed_password = get_password_hash(obj_in.password)
        obj_in_db = UserCreateDB(
            email=obj_in.email,
            phone=obj_in.phone,
            hashed_password=hashed_password,
        )
        return super().create(obj_in_db)

    # def register_user(self, user: UserRegister):
    #     await self._create_user(user)
    #     # TODO: сделать отправку email для верификации аккаунта


user_service = partial(UserService, User)
