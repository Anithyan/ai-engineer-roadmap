# app/main.py
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.logging_setup import setup_logging
from app.database import get_db
from app.schemas import ItemCreate, ItemOut

setup_logging()

app = FastAPI()

from app.api.routers import auth

app.include_router(auth.router)

from app.api.deps import get_current_user  # ← ta dépendance J11-PM
from app.models import Item, User  # ← ajoute User
from app.services import item_service  # ← ajoute cet import en haut


# POST /items — le serveur décide du propriétaire (jamais le client)
@app.post("/items", response_model=ItemOut, status_code=201)
def create_item(
    payload: ItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):  # ← exige un token
    item = Item(**payload.model_dump(), owner_id=current_user.id)  # ← owner = toi
    db.add(item)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="title already exists")
    db.refresh(item)  # recharge pour récupérer l'id généré par Postgres
    return item  # SQLAlchemy → Pydantic (via response_model)


@app.get("/items", response_model=list[ItemOut])
def list_items(db: Session = Depends(get_db)):
    return item_service.list_items(db)


@app.get("/items/{item_id}", response_model=ItemOut)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = item_service.get_item(db, item_id)
    if item is None:  # 🟥 la route décide : None → 404
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.delete("/items/{item_id}", status_code=204)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = db.get(Item, item_id)
    if item is None or item.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()


# app/main.py  (à ajouter)
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.limiter import limiter

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded, _rate_limit_exceeded_handler
)  # -> réponse 429 [C]
