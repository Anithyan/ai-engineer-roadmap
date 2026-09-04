# tests/conftest.py
import pytest
from app import models  # noqa: F401 → enregistre User ET Item sur Base.metadata

# tests/conftest.py  (à ajouter)
from app.core.limiter import limiter
from app.database import Base, get_db
from app.database import engine as app_engine
from app.main import (
    app as fastapi_app,  # renommé → évite la collision avec le package "app"
)
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# --- Base de test : même serveur Postgres, base "test_db" ---
TEST_URL = app_engine.url.set(database="test_db")
test_engine = create_engine(TEST_URL)
TestingSessionLocal = sessionmaker(bind=test_engine, autoflush=False)


# --- Override get_db → utilise la base de test (← J10) ---
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


fastapi_app.dependency_overrides[get_db] = override_get_db


# --- Fixtures ---
@pytest.fixture
def client():
    return TestClient(fastapi_app)


@pytest.fixture
def clean_db():
    Base.metadata.create_all(bind=test_engine)  # crée les tables users ET items
    yield
    Base.metadata.drop_all(bind=test_engine)  # tout effacé après le test


@pytest.fixture
def seed_test_user(clean_db):
    from app.core.security import hash_password
    from app.models import User

    db = TestingSessionLocal()
    user = User(email="demo@test.com", hashed_password=hash_password("secret123"))
    db.add(user)
    db.commit()
    db.refresh(user)  # récupère user.id
    db.close()
    return user


@pytest.fixture
def auth_headers(client, seed_test_user):
    resp = client.post(
        "/auth/token",  # ⚠️ VÉRIFIE : /auth/token ou /token (voir §Vérifs)
        data={
            "username": "demo@test.com",
            "password": "secret123",
        },  # data= (form OAuth2), username = EMAIL
    )
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def seed_15_items(seed_test_user):  # ← dépend du user existant
    from app.models import Item

    db = TestingSessionLocal()
    for i in range(1, 16):
        db.add(Item(title=f"Item {i}", owner_id=seed_test_user.id))  # ← même user
    db.commit()
    db.close()
    yield


@pytest.fixture(autouse=True)  # s'applique à TOUS les tests automatiquement
def _disable_rate_limit():
    limiter.enabled = False  # coupe le rate limiting pendant les tests
    yield
    limiter.enabled = True


@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db  # ← même pattern yield que ton get_db (J10)
    finally:
        db.close()
