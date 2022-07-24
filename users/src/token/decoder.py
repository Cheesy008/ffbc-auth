from fastapi import HTTPException
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette import status

from src.core.config import settings
from src.enums import TokenType
from src.models.token import BlacklistToken, OutstandingToken
from src.schemas import TokenEncodedData


class JWTDecoder:
    def __init__(self, db: Session, token: str):
        self.db = db
        self.token = token
        self.token_decoded_data = None

    @staticmethod
    def token_from_bearer_string(bearer_string: str):
        try:
            return bearer_string.split(" ")[1]
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid Bearer string",
            )

    def _decode(self) -> TokenEncodedData:
        try:
            payload = jwt.decode(self.token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return TokenEncodedData(**payload)
        except (jwt.JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )

    def verify(self, token_data: TokenEncodedData):
        black_list_token = (
            self.db.query(BlacklistToken)
            .join(OutstandingToken)
            .filter(
                OutstandingToken.jti == token_data.jti,
                OutstandingToken.user_id == token_data.user_id,
            )
            .first()
        )
        if black_list_token:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token in blacklist",
            )

    def decode_token(
        self, token_type: TokenType, add_token_to_blacklist: bool = False
    ) -> TokenEncodedData:
        self.token_decoded_data = self._decode()
        self.verify(self.token_decoded_data)
        if self.token_decoded_data.token_type != token_type:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Token type must be {token_type.title()}",
            )
        if add_token_to_blacklist:
            self.add_to_blacklist()
        return self.token_decoded_data

    def add_to_blacklist(self):
        outstanding_token = (
            self.db.query(OutstandingToken)
            .filter(
                OutstandingToken.jti == self.token_decoded_data.jti,
                OutstandingToken.user_id == self.token_decoded_data.user_id,
            )
            .first()
        )
        if not outstanding_token:
            outstanding_token = OutstandingToken(
                user_id=self.token_decoded_data.user_id,
                jti=self.token_decoded_data.jti,
                expires_at=self.token_decoded_data.exp,
                token=self.token,
            )
            self.db.add(outstanding_token)
            self.db.commit()
            self.db.refresh(outstanding_token)
        blacklist_token = BlacklistToken(outstanding_token=outstanding_token)
        self.db.add(blacklist_token)
        self.db.commit()
        self.db.refresh(blacklist_token)
