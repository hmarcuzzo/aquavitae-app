from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def validate_hash(password, hashed):
    return pwd_context.verify(password, hashed)


def generate_hash(password):
    return pwd_context.hash(password)
