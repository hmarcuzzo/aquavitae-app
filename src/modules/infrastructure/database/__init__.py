from sqlalchemy.orm import Session

import src.modules.infrastructure.database.soft_delete_filter
from .session import SessionLocal


def get_db() -> Session:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
