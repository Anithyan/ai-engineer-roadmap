# tests/test_users.py
import pytest


# --- 1) LOGIN OK → 200 + token  (le cas nominal) --------------------------
def test_login_success(client, seed_test_user):
    resp = client.post(
        "/auth/token",  # route login (prefix /auth + /token)
        data={
            "username": "demo@test.com",
            "password": "secret123",
        },  # data= (form OAuth2), username = EMAIL
    )
    assert resp.status_code == 200
    assert "access_token" in resp.json()  # le token est bien présent


# --- 2) LOGIN KO → 401  (mauvais identifiants, 3 cas) ---------------------
@pytest.mark.parametrize(
    "email, password",
    [
        ("demo@test.com", "wrong_password"),  # bon email, mauvais mot de passe
        ("inconnu@test.com", "secret123"),  # email inexistant
        ("demo@test.com", "another_wrong_one"),  # mot de passe vide
    ],
    ids=["wrong_password", "unknown_email", "empty_password"],
)
def test_login_invalid_credentials(client, seed_test_user, email, password):
    resp = client.post("/auth/token", data={"username": email, "password": password})
    assert resp.status_code == 401


# --- 3) ROUTE PROTÉGÉE → 401 SANS token  (2 cas) --------------------------
# get_current_user renvoie 401 si le header Authorization manque ou est invalide.
@pytest.mark.parametrize(
    "headers",
    [
        {},  # aucun header → pas de token
        {"Authorization": "Bearer faux_token"},  # token bidon → invalide
    ],
    ids=["no_token", "invalid_token"],
)
def test_users_me_requires_auth(client, seed_test_user, headers):
    resp = client.get(
        "/auth/users/me", headers=headers
    )  # ⚠️ URL = /auth/users/me (prefix /auth !)
    assert resp.status_code == 401


# --- 4) ROUTE PROTÉGÉE → 200 AVEC token  (le cas nominal) -----------------
def test_users_me_with_token(client, auth_headers):
    resp = client.get(
        "/auth/users/me", headers=auth_headers
    )  # auth_headers = token valide
    assert resp.status_code == 200
    assert resp.json()["email"] == "demo@test.com"  # ⚠️ "email", PAS "username"
