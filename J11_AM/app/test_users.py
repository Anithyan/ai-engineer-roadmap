# test_users.py
def test_create_user(client, clean_db):  # écrire un item marche
    r = client.post("/items/", json={"title": "Alice", "description": "alice@test.com"})
    assert r.status_code == 201
    assert r.json()["title"] == "Alice"


def test_list_is_empty(client, clean_db):  # ← PROUVE l'isolation
    assert client.get("/items/").json() == []  # base vide, quoi qu'il ait précédé


def test_get_user_by_id(client, clean_db):  # relire un item par son id
    created = client.post(
        "/items/", json={"title": "Bob", "description": "bob@test.com"}
    ).json()
    r = client.get(f"/items/{created['id']}")
    assert r.status_code == 200
    assert r.json()["description"] == "bob@test.com"


def test_missing_user_404(client, clean_db):  # un id inexistant → 404
    assert client.get("/items/999999").status_code == 404


def test_duplicate_email_rejected(client, clean_db):  # ← PROUVE la valeur "intégration"
    payload = {"title": "Carol", "description": "carol@test.com"}
    assert client.post("/items/", json=payload).status_code in (200, 201)
    assert client.post("/items/", json=payload).status_code in (
        400,
        409,
    )  # contrainte UNIQUE de Postgres


def test_delete_user(client, clean_db):  # supprimer un item
    created = client.post(
        "/items/", json={"title": "Dave", "description": "dave@test.com"}
    ).json()
    assert client.delete(f"/items/{created['id']}").status_code == 204
    assert client.get(f"/items/{created['id']}").status_code == 404
