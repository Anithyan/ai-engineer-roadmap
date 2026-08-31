# app/api/deps.py
from typing import Annotated

import jwt
from app.core.security import ALGORITHM, SECRET_KEY
from app.database import get_db
from app.models import User
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")  # [B]


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # [A]
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:  # ⚠️ PyJWT 2.x : couvre AUSSI l'expiration
        raise credentials_exception
    user = db.scalar(select(User).where(User.email == username))
    if user is None:
        raise credentials_exception
    return user
