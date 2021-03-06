from functools import partial

from fastapi import HTTPException, UploadFile

from src.core.base_service import BaseService, ModelType
from src.core.security import get_password_hash, verify_password
from src.models import User
from src.schemas import UserCreate, UserCreateDB, UserUpdate
from src.utils import write_file_on_disk


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
            raise HTTPException(status_code=400, detail="This email has been already registered")
        hashed_password = get_password_hash(obj_in.password)
        obj_in_db = UserCreateDB(
            email=obj_in.email,
            phone=obj_in.phone,
            hashed_password=hashed_password,
        )
        return super().create(obj_in_db)

    def upload_avatar(self, current_user: User, avatar: UploadFile):
        file_location = write_file_on_disk(avatar, "user/avatar/")
        current_user.avatar = file_location
        self.db.commit()

    # def register_user(self, user: UserRegister):
    #     self._create_user(user)
    #     # TODO: сделать отправку email для верификации аккаунта


user_service = partial(UserService, User)
