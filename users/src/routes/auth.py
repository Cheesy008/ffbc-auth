from fastapi import Depends, APIRouter, Response, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.core.security import create_access_and_refresh_tokens
from src.db.db import get_db
from src.dependencies import get_user_from_refresh_token, get_current_user
from src.models import User
from src.schemas import UserCreate, TokenResponse
from src.schemas.user import UserBase
from src.services import user_service

auth_router = APIRouter()


@auth_router.post("/register")
async def register_user(user: UserCreate, session: Session = Depends(get_db)):
    service = user_service(session)
    service.create(user)
    return Response(status_code=200)


@auth_router.post("/login/access-token", response_model=TokenResponse)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = user_service(db).authenticate(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    return create_access_and_refresh_tokens(user.id)


@auth_router.post("/login/refresh-token", response_model=TokenResponse)
def login_refresh_token(user: User = Depends(get_user_from_refresh_token)):
    return create_access_and_refresh_tokens(user.id)


@auth_router.get("/user/me", response_model=UserBase)
def get_current_user(
    db: Session = Depends(get_db),
    current_user: UserBase = Depends(get_current_user),
):
    pass
