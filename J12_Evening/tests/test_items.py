# tests/test_items.py
import pytest


# --- 1) VALIDATION → 422  (4 cas) -----------------------------------------
# Adapté à ton modèle Item : title (obligatoire) + description (optionnel).
# ⚠️ Vérifie ItemCreate dans schemas.py. Si un cas renvoie 201 au lieu de 422,
#    c'est que ton schéma ne contraint pas ce champ → validation manquante trouvée.
@pytest.mark.parametrize(
    "payload",
    [
        {},  # title manquant
        {"description": "sans titre"},  # title manquant (description seule)
        {"title": 12345},  # title n'est pas un str
        {"title": None},  # title est null
    ],
    ids=["missing_title", "only_description", "title_not_string", "title_null"],
)
def test_create_item_invalid_payload(client, auth_headers, payload):
    resp = client.post("/items", json=payload, headers=auth_headers)  # ← token
    assert resp.status_code == 422


# --- 2) NOT FOUND → 404  (3 cas) ------------------------------------------
@pytest.mark.parametrize(
    "item_id",
    [999999, 123456, 888888],
    ids=["id_999999", "id_123456", "id_888888"],
)
def test_get_item_not_found(client, clean_db, auth_headers, item_id):
    resp = client.get(f"/items/{item_id}", headers=auth_headers)  # ← token
    assert resp.status_code == 404


# --- 3) PAGINATION → 200 + bon nombre  (3 cas) ----------------------------
# ⚠️ Suppose que GET /items lit les query params skip & limit (← J11-AM).
@pytest.mark.parametrize(
    "skip, limit, expected_count",
    [
        (0, 10, 10),  # 1re page
        (0, 5, 5),  # petite limite
        (10, 10, 5),  # 15 items en base → il en reste 5
    ],
    ids=["first_page", "small_limit", "last_page"],
)
def test_pagination(client, seed_15_items, auth_headers, skip, limit, expected_count):
    resp = client.get(
        f"/items?skip={skip}&limit={limit}", headers=auth_headers
    )  # ← token
    assert resp.status_code == 200
    assert len(resp.json()) == expected_count
