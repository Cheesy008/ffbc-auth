from datetime import datetime

from pydantic import BaseModel

from src.enums import TokenType


class TokenSub(BaseModel):
    token_type: TokenType
    user_id: int

    class Config:
        use_enum_values = True


class TokenEncodedData(BaseModel):
    token_type: TokenType
    jti: str
    user_id: int
    exp: datetime


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
