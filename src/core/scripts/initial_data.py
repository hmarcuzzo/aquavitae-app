from datetime import datetime

from src.core.constants.enum.user_role import UserRole
from src.core.utils.hash_utils import generate_hash
from src.modules.infrastructure.database.session import engine
from src.modules.infrastructure.user.entities.user_entity import User


def create_initial_users():
    username = input("Username [admin]: ") or "admin"
    password = input("Password [admin]: ") or "admin"

    if "@" not in username:
        username = f"{username}@aquavitae.com"

    print(f'Creating user "{username}" with password "{password}"...\n')

    now = datetime.now()
    user_admin = {
        "created_at": now,
        "updated_at": now,
        "email": username,
        "password": generate_hash(password),
        "role": UserRole.ADMIN,
    }
    engine.execute(User.__table__.insert().values(**user_admin))


if __name__ == "__main__":
    create_initial_users()
