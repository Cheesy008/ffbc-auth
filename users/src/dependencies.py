from fastapi import Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.core.security import JWTDecoder
from src.db.db import get_db
from src.enums import TokenType
from src.models import User
from src.services import user_service

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/login/access-token")


def get_current_user(db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)) -> User:
    decoder = JWTDecoder(token)
    token_data = decoder.decode_token(TokenType.ACCESS)
    user = user_service(db).get(id=token_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_user_from_refresh_token(
    db: Session = Depends(get_db), refresh_token: str = Body(..., embed=True)
):
    decoder = JWTDecoder(refresh_token)
    token_data = decoder.decode_token(TokenType.REFRESH)
    user = user_service(db).get(id=token_data.user_id)
    return user
