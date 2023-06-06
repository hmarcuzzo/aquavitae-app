from src.core.constants.enum.user_role import UserRole
from src.modules.infrastructure.database import get_db
from src.modules.infrastructure.user.dto.create_user_dto import CreateUserWithRoleDto
from src.modules.infrastructure.user.entities.user_entity import User
from src.modules.infrastructure.user.user_interface import UserInterface


def check_if_admin_exist():
    with next(get_db()) as db_session:
        user = db_session.query(User).where(User.role == UserRole.ADMIN).first()
        return user is not None


async def create_initial_users():
    if not check_if_admin_exist():
        username = input("Username [admin]: ") or "admin"
        password = input("Password [admin]: ") or "admin"

        if "@" not in username:
            username = f"{username}@aquavitae.com"

        print(f'Creating user "{username}" with password "{password}"...\n')

        user_interface = UserInterface()
        with next(get_db()) as db_session:
            await user_interface.create_user_with_role(
                CreateUserWithRoleDto(
                    **{"email": username, "password": password, "role": UserRole.ADMIN}
                ),
                db_session,
            )
    else:
        print("Admin already exists. Skipping creation.\n")
