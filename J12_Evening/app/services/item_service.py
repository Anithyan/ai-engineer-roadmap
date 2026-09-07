# app/services/item_service.py
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Item
from app.schemas import ItemCreate

# ⚠️ AUCUN "from fastapi import ..." ici.


class DuplicateTitleError(Exception):
    """Le titre existe déjà. Erreur MÉTIER, pas HTTP."""


def get_item(db: Session, item_id: int) -> Item | None:
    """Item par id, sans contrôle de propriétaire (usage interne)."""
    return db.get(Item, item_id)


def get_item_for_owner(db: Session, item_id: int, owner_id: int) -> Item | None:
    """Item SEULEMENT s'il appartient à owner_id, sinon None (règle BOLA)."""
    item = get_item(db, item_id)  # DRY : réutilise get_item
    if item is None or item.owner_id != owner_id:
        return None
    return item


def list_items(db: Session, skip: int = 0, limit: int = 100):
    return db.scalars(select(Item).offset(skip).limit(limit)).all()


def create_item_for_owner(db: Session, data: ItemCreate, owner_id: int) -> Item:
    """Crée un item pour owner_id ; lève DuplicateTitleError si le titre existe déjà."""
    item = Item(
        **data.model_dump(), owner_id=owner_id
    )  # le serveur fixe le propriétaire
    db.add(item)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DuplicateTitleError(data.title)  # métier, PAS de 409 ici
    db.refresh(item)
    return item


def delete_item_for_owner(db: Session, item_id: int, owner_id: int) -> bool:
    """Supprime l'item s'il appartient à owner_id. True si supprimé, False sinon."""
    item = get_item_for_owner(
        db, item_id, owner_id
    )  # DRY : réutilise la règle d'ownership
    if item is None:
        return False
    db.delete(item)
    db.commit()
    return True
