# app/services/item_service.py
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Item

# ⚠️ AUCUN "from fastapi import ..." ici — volontaire.


def get_item(db: Session, item_id: int) -> Item | None:
    """Renvoie l'item par son id, ou None s'il n'existe pas."""
    return db.get(Item, item_id)  # ← db.get de J10


def list_items(db: Session) -> list[Item]:
    """Renvoie tous les items."""
    return list(db.scalars(select(Item)).all())  # ← select() de J10
