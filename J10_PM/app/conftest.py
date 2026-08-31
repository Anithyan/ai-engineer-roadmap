# conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models  # noqa: F401  (enregistre la table users)
from app.database import Base, get_db
from app.database import engine as app_engine
from app.main import (
    app as fastapi_app,  # renommé → évite la collision avec le package "app"
)

# URL de test dérivée de ton app : même driver + mêmes identifiants, base "test_db"
TEST_URL = app_engine.url.set(database="test_db")
test_engine = create_engine(TEST_URL)
TestingSessionLocal = sessionmaker(bind=test_engine, autoflush=False)

assert test_engine.url.database == "test_db", "STOP : les tests ne visent pas test_db !"


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


fastapi_app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    return TestClient(fastapi_app)


@pytest.fixture
def clean_db():
    Base.metadata.create_all(bind=test_engine)  # tables fraîches avant chaque test
    yield
    Base.metadata.drop_all(bind=test_engine)  # tout effacé après
