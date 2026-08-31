from app.core.security import hash_password
from app.database import engine as app_engine
from app.models import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# même base de test que ton conftest (test_db)
_TestSession = sessionmaker(bind=create_engine(app_engine.url.set(database="test_db")))


def _seed_user(email, password):
    db = _TestSession()
    db.add(User(email=email, hashed_password=hash_password(password)))
    db.commit()
    db.close()


def _token(client, email, password):
    r = client.post("/auth/token", data={"username": email, "password": password})
    return r.json()["access_token"]


def test_user_cannot_read_another_users_item(client, clean_db):
    _seed_user("alice@test.com", "pwd12345")
    _seed_user("bob@test.com", "pwd12345")
    tok_a = _token(client, "alice@test.com", "pwd12345")
    tok_b = _token(client, "bob@test.com", "pwd12345")

    item_id = client.post(
        "/items",
        json={"title": "secret alice"},
        headers={"Authorization": f"Bearer {tok_a}"},
    ).json()["id"]

    # Bob tente avec SON token → doit être refusé
    assert (
        client.get(
            f"/items/{item_id}", headers={"Authorization": f"Bearer {tok_b}"}
        ).status_code
        == 404
    )
    # Alice, elle, accède bien à son item
    assert (
        client.get(
            f"/items/{item_id}", headers={"Authorization": f"Bearer {tok_a}"}
        ).status_code
        == 200
    )
