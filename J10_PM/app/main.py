# app/main.py
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Item
from app.schemas import ItemCreate, ItemOut

app = FastAPI()


@app.post("/items", response_model=ItemOut, status_code=201)
def create_item(payload: ItemCreate, db: Session = Depends(get_db)):
    item = Item(**payload.model_dump())  # Pydantic → SQLAlchemy
    db.add(item)
    try:  # met l'objet dans la session (le "panier")
        db.commit()  # ← ÉCRIT réellement en base
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="title already exists")
    db.refresh(item)  # recharge pour récupérer l'id généré par Postgres
    return item  # SQLAlchemy → Pydantic (via response_model)


@app.get("/items", response_model=list[ItemOut])
def list_items(db: Session = Depends(get_db)):
    return db.scalars(select(Item)).all()  # SELECT * FROM items → liste d'objets


@app.get("/items/{item_id}", response_model=ItemOut)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.get(Item, item_id)  # SELECT par clé primaire
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
