import bcrypt

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def generate_salt():
    return bcrypt.gensalt().decode()

def verify_password(plain_pw: str, hashed_pw: str) -> str:
    return pwd_context.verify(plain_pw, hashed_pw)

def get_password_hash(pw: str) -> str:
    return pwd_context.hash(pw)