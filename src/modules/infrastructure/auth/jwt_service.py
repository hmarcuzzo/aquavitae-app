from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from config import TOKEN_ALGORITHM, TOKEN_EXPIRATION_MINUTES, TOKEN_SECRET_KEY
from src.core.constants.enum.user_role import UserRole
from src.core.types.exceptions_type import UnauthorizedException
from src.modules.infrastructure.auth.dto.token_payload_dto import TokenPayloadDto
from src.modules.infrastructure.database import get_db
from src.modules.infrastructure.user import User
from src.modules.infrastructure.user.user_interface import UserInterface

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
user_interface = UserInterface()

credentials_exception = UnauthorizedException("Could not validate credentials")


def create_access_token(data: dict) -> TokenPayloadDto:
    to_encode = data.copy()
    expire = datetime.now().astimezone() + timedelta(minutes=TOKEN_EXPIRATION_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, TOKEN_SECRET_KEY, algorithm=TOKEN_ALGORITHM)

    return TokenPayloadDto(expires_in=expire, access_token=encoded_jwt)


def verify_token(token: str, data: str) -> str:
    try:
        payload = jwt.decode(token, TOKEN_SECRET_KEY, algorithms=[TOKEN_ALGORITHM])
        user_data: str = payload.get(data)
        if user_data is None:
            raise credentials_exception
        return user_data
    except JWTError:
        raise credentials_exception


async def get_current_user(
    data: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    user_id = verify_token(data, "user_id")
    return await user_interface.find_one_user(
        db, find_data={"where": User.id == user_id}
    )


async def get_current_user_role(data: str = Depends(oauth2_scheme)) -> UserRole:
    user_role = verify_token(data, "user_role")
    return UserRole(user_role)
