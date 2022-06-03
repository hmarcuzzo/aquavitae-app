from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from config import TOKEN_ALGORITHM, TOKEN_EXPIRATION_MINUTES, TOKEN_SECRET_KEY
from src.core.types.exceptions_type import UnauthorizedException
from src.modules.infrastructure.auth.dto.token_payload_dto import TokenPayloadDto
from src.modules.infrastructure.database import get_db
from src.modules.infrastructure.user.entities.user_entity import User
from src.modules.infrastructure.user.user_interface import UserInterface

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
user_interface = UserInterface()


def create_access_token(data: dict) -> TokenPayloadDto:
    to_encode = data.copy()
    expire = datetime.now().astimezone() + timedelta(minutes=TOKEN_EXPIRATION_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, TOKEN_SECRET_KEY, algorithm=TOKEN_ALGORITHM)

    return TokenPayloadDto(expires_in=expire, access_token=encoded_jwt)


async def verify_token(token: str, credentials_exception, db: Session) -> User:
    try:
        payload = jwt.decode(token, TOKEN_SECRET_KEY, algorithms=[TOKEN_ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        return await user_interface.find_one_user(db, find_data={'where': User.id == user_id})
    except JWTError:
        raise credentials_exception


async def get_current_user(data: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = UnauthorizedException('Could not validate credentials')
    return await verify_token(data, credentials_exception, db)
