from typing import List

from sqlalchemy.orm import Session

from .entities.user_entity import User


class UserRepository:
    def find_user_by_email(self, email: str, db_session: Session) -> User:
        return db_session.query(User).filter(User.email == email).first()

    def create_user(self, user: User, db_session: Session) -> User:
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    def get_all_users(self, db_session: Session) -> List[User]:
        return db_session.query(User).all()

    def find_user_by_id(self, user_id, db_session: Session) -> User:
        return db_session.query(User).filter(User.id == user_id).first()

    def delete_user_by_id(self, user_id, db_session: Session):
        db_session.query(User).filter(User.id == user_id).delete()
