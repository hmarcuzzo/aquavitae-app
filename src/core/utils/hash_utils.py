from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def validate_hash(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def generate_hash(password: str) -> str:
    return pwd_context.hash(password)
