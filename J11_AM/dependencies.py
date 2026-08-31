from typing import Annotated

from app.database import get_db  # ton get_db de J10 (celui qui yield une Session)
from fastapi import Depends
from sqlalchemy.orm import Session

# type alias réutilisable : "une Session fournie par get_db"
DbDep = Annotated[Session, Depends(get_db)]

from fastapi import Query


def pagination_params(
    skip: Annotated[int, Query(ge=0)] = 0,  # défaut 0, doit être ≥ 0
    limit: Annotated[int, Query(ge=1, le=100)] = 10,  # défaut 10, entre 1 et 100
) -> dict:
    return {"skip": skip, "limit": limit}


PaginationDep = Annotated[dict, Depends(pagination_params)]
