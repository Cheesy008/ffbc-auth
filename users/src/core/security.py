from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.schemas.token import TokenResponse
from src.token.encoder import AccessToken, RefreshToken

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_and_refresh_tokens(db: Session, user_id: int) -> TokenResponse:
    access_token = AccessToken(db, user_id).create_token()
    refresh_token = RefreshToken(db, user_id).create_token()
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)
