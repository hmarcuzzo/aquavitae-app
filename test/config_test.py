import pytest

from src.modules.infrastructure.user.entities.user_entity import User


@pytest.fixture(autouse=True)
def create_dummy_user():
    """Fixture to execute asserts before and after a test run."""
    from config_test_db import override_get_db
    database = next(override_get_db())
    new_user = User(name="John", email="john@gmail.com", password="12345678")
    database.add_user(new_user)
    database.commit()

    yield  # Execute the test

    # Teardown
    database.query(User).filter(User.email == "john@gmail.com").delete()
    database.commit()