# app/models.py
from datetime import datetime

from sqlalchemy import (
    ForeignKey,  # en haut du fichier
    String,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)  # NOT NULL + PK
    email: Mapped[str] = mapped_column(String(255), unique=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    hashed_password: Mapped[str] = mapped_column(nullable=False)


class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(
        String(255), unique=True
    )  # NOT NULL (pas de | None)
    description: Mapped[str | None] = mapped_column(String(500))  # nullable (| None)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    is_active: Mapped[bool] = mapped_column(server_default=text("true"))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))  # ← NOUVEAU
