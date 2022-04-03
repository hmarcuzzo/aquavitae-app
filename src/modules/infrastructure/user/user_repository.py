from typing import Optional

from sqlalchemy.orm import Session

from .entities.user_entity import User


class UserRepository:
    def find_user_by_email(self, email: str, db_session: Session) -> Optional[User]:
        return db_session.query(User).filter(User.email == email).first()

    def create_user(self, user: User, db_session: Session) -> User:
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user
