# app/api/routers/auth.py
from datetime import timedelta
from typing import Annotated

from app.core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    verify_password,
)
from app.database import get_db  # ← ta dépendance de session J10
from app.models import User  # ← ton model User J10
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["auth"])


class Token(BaseModel):
    access_token: str
    token_type: str


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    user = db.scalar(select(User).where(User.email == username))  # ← select() de J10
    if user is None:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


from app.core.limiter import limiter
from fastapi import Request


@router.post("/token")  # 1) route AU-DESSUS
@limiter.limit("5/minute")  # 2) limit EN-DESSOUS
def login_for_access_token(
    request: Request,  # 3) OBLIGATOIRE pour SlowAPI
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(  # ← tes HTTPException de J9
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.email},  # claim sub = identité
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=access_token, token_type="bearer")


# app/api/routers/auth.py  (à ajouter)
from app.api.deps import get_current_user


class UserPublic(BaseModel):
    id: int
    email: str
    model_config = {"from_attributes": True}  # lit depuis l'objet SQLAlchemy


@router.get("/users/me", response_model=UserPublic)
def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
