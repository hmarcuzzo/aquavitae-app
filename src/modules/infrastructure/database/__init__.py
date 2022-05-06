from sqlalchemy.orm import Session

from src.modules.infrastructure.database.session import SessionLocal


def get_db() -> Session:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
