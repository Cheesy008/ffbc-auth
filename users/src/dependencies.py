from fastapi import Depends, HTTPException, Body, UploadFile
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.constants import IMAGE_EXTENSIONS
from src.db.db import get_db
from src.enums import TokenType
from src.models import User
from src.services import user_service
from src.token.decoder import JWTDecoder
from src.utils.file import validate_file_extension

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/login/access-token")

auth_scheme = HTTPBearer()


def get_current_user(
    db: Session = Depends(get_db),
    auth_credentials: HTTPAuthorizationCredentials = Depends(auth_scheme),
) -> User:
    token = JWTDecoder.token_from_bearer_string(auth_credentials.credentials)
    decoder = JWTDecoder(db, token)
    token_data = decoder.decode_token(TokenType.ACCESS)
    user = user_service(db).get(id=token_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_user_from_refresh_token(
    db: Session = Depends(get_db), refresh_token: str = Body(..., embed=True)
):
    decoder = JWTDecoder(db, refresh_token)
    token_data = decoder.decode_token(TokenType.REFRESH, add_token_to_blacklist=True)
    user = user_service(db).get(id=token_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def validate_user_avatar(avatar: UploadFile):
    validate_file_extension(filename=avatar.filename, allowed_file_extensions=IMAGE_EXTENSIONS)
    return avatar
