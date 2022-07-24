from fastapi import Depends, APIRouter, Response, HTTPException, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.core.security import create_access_and_refresh_tokens
from src.db.db import get_db
from src.dependencies import get_user_from_refresh_token, get_current_user, validate_user_avatar
from src.models import User
from src.schemas import UserCreate, TokenResponse
from src.schemas.user import UserBase, UserUpdate, UserResponse
from src.services import user_service

auth_router = APIRouter()


@auth_router.post("/register")
def register_user_route(user: UserCreate, session: Session = Depends(get_db)):
    service = user_service(session)
    service.create(user)
    return Response(status_code=200)


@auth_router.post("/login/access-token", response_model=TokenResponse)
def login_access_token_route(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = user_service(db).authenticate(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return create_access_and_refresh_tokens(db, user.id)


@auth_router.post("/login/refresh-token", response_model=TokenResponse)
def login_refresh_token_route(
    db: Session = Depends(get_db), user: User = Depends(get_user_from_refresh_token)
):
    return create_access_and_refresh_tokens(db, user.id)


@auth_router.get("/user/me", response_model=UserResponse)
def get_current_user_route(current_user: UserBase = Depends(get_current_user)):
    return current_user


@auth_router.patch("/user/me", response_model=UserResponse)
def update_current_user_route(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    service = user_service(session)
    user = service.update(db_obj=current_user, obj_in=user_update)
    return user


@auth_router.patch("/user/me/update-avatar", response_model=UserResponse)
def update_current_user_avatar_route(
    avatar: UploadFile = Depends(validate_user_avatar),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    service = user_service(session)
    service.upload_avatar(current_user, avatar)
    return Response(status_code=200)
