# app/core/security.py
from datetime import datetime, timedelta, timezone

import jwt
from app.core.config import settings
from pwdlib import PasswordHash

# ⚠️ DETTE: en dur aujourd'hui, à migrer en variable d'env (J12-PM).
# Génère la tienne: openssl rand -hex 32
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

password_hash = PasswordHash.recommended()  # <- configure Argon2 pour toi [A]


def hash_password(plain_password: str) -> str:
    return password_hash.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})  # claim d'expiration
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # [A]
