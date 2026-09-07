# app/main.py
from fastapi import Depends, FastAPI, HTTPException
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.api.deps import get_current_user  # ← ta dépendance J11-PM
from app.api.routers import auth
from app.core.limiter import limiter
from app.core.logging_setup import setup_logging
from app.database import get_db
from app.models import User  # ← ajoute User
from app.schemas import ItemCreate, ItemOut
from app.services import item_service  # ← ajoute cet import en haut
from app.services.item_service import DuplicateTitleError

setup_logging()

app = FastAPI()

app.include_router(auth.router)


# app/main.py
@app.get("/health")
def health(db: Session = Depends(get_db)):
    try:
        db.execute(
            text("SELECT 1")
        )  # SQLAlchemy 2.0 exige text() pour du SQL brut (← J11)
    except SQLAlchemyError:
        raise HTTPException(status_code=503, detail="database unavailable")
    return {"status": "ok"}


@app.post("/items", response_model=ItemOut, status_code=201)
def create_item(
    payload: ItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return item_service.create_item_for_owner(db, payload, current_user.id)
    except DuplicateTitleError:  # métier → 409
        raise HTTPException(status_code=409, detail="title already exists")


@app.get("/items", response_model=list[ItemOut])
def list_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return item_service.list_items(db, skip=skip, limit=limit)


@app.get("/items/{item_id}", response_model=ItemOut)
def get_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):  # ← REMET l'auth
    item = item_service.get_item_for_owner(
        db, item_id, current_user.id
    )  # ← REMET l'ownership
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.delete("/items/{item_id}", status_code=204)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not item_service.delete_item_for_owner(db, item_id, current_user.id):
        raise HTTPException(status_code=404, detail="Item not found")


app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,  # type: ignore[arg-type]
)  # -> réponse 429 [C]
