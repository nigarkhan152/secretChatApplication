import secrets
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from config.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_secret_key():
    return secrets.token_urlsafe(32)

def hash_secret_key(key: str):
    return pwd_context.hash(key)

def verify_secret_key(plain_key: str, hashed_key: str):
    return pwd_context.verify(plain_key, hashed_key)

def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    data.update({"exp": expire})
    return jwt.encode(data,settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


