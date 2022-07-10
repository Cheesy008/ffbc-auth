from datetime import datetime, timedelta
from typing import TypedDict
from uuid import uuid4

from jose import jwt
from sqlalchemy.orm import Session

from src.core.config import settings
from src.enums import TokenType
from src.models import OutstandingToken

ALGORITHM = "HS256"


class TokenPayloadDict(TypedDict, total=False):
    token_type: TokenType
    jti: str
    user_id: int
    exp: datetime


class JWTEncoder:
    token_type = None
    lifetime = None

    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id = user_id

    @property
    def payload(self) -> TokenPayloadDict:
        exp = datetime.utcnow() + timedelta(minutes=self.lifetime)
        jti = uuid4().hex
        return TokenPayloadDict(user_id=self.user_id, token_type=self.token_type, exp=exp, jti=jti)

    def _encode_payload(self) -> str:
        encoded_jwt = jwt.encode(self.payload, settings.SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def _save_token_to_db(self, token: str):
        db_obj = OutstandingToken(
            user_id=self.payload["user_id"],
            jti=self.payload["jti"],
            expires_at=self.payload["exp"],
            token=token,
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)

    def create_token(self):
        token = self._encode_payload()
        self._save_token_to_db(token)
        return token


class AccessToken(JWTEncoder):
    token_type = TokenType.ACCESS
    lifetime = settings.ACCESS_TOKEN_EXPIRE_MINUTES


class RefreshToken(JWTEncoder):
    token_type = TokenType.ACCESS
    lifetime = settings.REFRESH_TOKEN_EXPIRE_MINUTES
