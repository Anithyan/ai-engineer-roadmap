# app/schemas.py
from pydantic import BaseModel, ConfigDict


class ItemCreate(BaseModel):  # ce que le CLIENT envoie (entrée)
    title: str
    description: str | None = None


class ItemOut(BaseModel):  # ce que l'API RENVOIE (sortie)
    id: int
    title: str
    description: str | None
    # autorise Pydantic à LIRE les attributs d'un objet SQLAlchemy :
    model_config = ConfigDict(from_attributes=True)
