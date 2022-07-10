import json
from datetime import timedelta, datetime

from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext
from pydantic import ValidationError
from starlette import status

from src.core.config import settings
from src.enums import TokenType
from src.schemas.token import TokenSub, TokenResponse, TokenEncodedData

ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# region JWT


class JWTDecoder:
    def __init__(self, token: str):
        self.token = token

    def _decode(self) -> TokenSub:
        try:
            payload = jwt.decode(self.token, settings.SECRET_KEY, algorithms=[ALGORITHM])
            validated_data = TokenEncodedData(**payload)
            valid_json_string = validated_data.sub.replace("'", '"')
            return TokenSub(**json.loads(valid_json_string))
        except (jwt.JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )

    def decode_token(self, token_type: TokenType):
        token_data = self._decode()
        if token_data.token_type != token_type:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"TokenResponse type must be {token_type.title()}",
            )
        return token_data


def create_token(subject: TokenSub, expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = TokenEncodedData(exp=expire, sub=str(subject.dict()))
    encoded_jwt = jwt.encode(to_encode.dict(), settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_access_and_refresh_tokens(user_id: int) -> TokenResponse:
    access_token = create_token(
        TokenSub(token_type=TokenType.ACCESS, user_id=user_id),
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_token(
        TokenSub(token_type=TokenType.REFRESH, user_id=user_id),
        expires_delta=timedelta(days=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


# endregion
