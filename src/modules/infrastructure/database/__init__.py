from sqlalchemy.orm import Session

from .session import SessionLocal


def get_db() -> Session:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
