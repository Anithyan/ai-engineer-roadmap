"""Tests qui prouvent que Pydantic accepte le valide ET rejette l'invalide."""

import pytest
from pydantic import ValidationError
from src.pydantic_nested import User
from src.pydantic_validation import UserSignup

# ====== HAPPY PATH ======


def test_user_valid_minimal() -> None:
    """User valide avec données minimales (pas de secondary_addresses)."""
    user = User.model_validate(
        {
            "user_id": 1,
            "name": "Alice",
            "email": "alice@example.com",
            "age": 30,
            "primary_address": {
                "street": "1 rue X",
                "city": "Paris",
                "postal_code": "75001",
            },
        }
    )
    assert user.user_id == 1
    assert user.primary_address.country == "France"  # défaut
    assert user.secondary_addresses == []  # défaut factory


# ====== 5 CAS DE REJET DISTINCTS (critère de done) ======


def test_reject_missing_required_field() -> None:
    """Cas 1 : champ requis manquant (email)."""
    with pytest.raises(ValidationError) as exc_info:
        User.model_validate(
            {
                "user_id": 1,
                "name": "Alice",
                "age": 30,
                "primary_address": {
                    "street": "1 rue X",
                    "city": "Paris",
                    "postal_code": "75001",
                },
                # email manquant
            }
        )
    errors = exc_info.value.errors()
    assert any(err["loc"] == ("email",) and err["type"] == "missing" for err in errors)


def test_reject_wrong_type() -> None:
    """Cas 2 : mauvais type sur un champ (age = str non convertible)."""
    with pytest.raises(ValidationError) as exc_info:
        User.model_validate(
            {
                "user_id": 1,
                "name": "Alice",
                "email": "alice@example.com",
                "age": "pas un nombre",  # int attendu, str non numérique reçue
                "primary_address": {
                    "street": "1 rue X",
                    "city": "Paris",
                    "postal_code": "75001",
                },
            }
        )
    errors = exc_info.value.errors()
    assert any(err["loc"] == ("age",) for err in errors)


def test_reject_constraint_violated() -> None:
    """Cas 3 : contrainte métier violée (username trop court)."""
    with pytest.raises(ValidationError) as exc_info:
        UserSignup.model_validate(
            {
                "username": "ab",  # min_length=3
                "email": "alice@example.com",
                "age": 25,
                "password": "longenough123",
            }
        )
    errors = exc_info.value.errors()
    assert any("at least 3 characters" in err["msg"] for err in errors)


def test_reject_nested_invalid() -> None:
    """Cas 4 : sous-modèle (Address) invalide (postal_code mauvais format)."""
    with pytest.raises(ValidationError) as exc_info:
        User.model_validate(
            {
                "user_id": 1,
                "name": "Alice",
                "email": "alice@example.com",
                "age": 30,
                "primary_address": {
                    "street": "1 rue X",
                    "city": "Paris",
                    "postal_code": "ABCDE",  # doit être 5 chiffres
                },
            }
        )
    errors = exc_info.value.errors()
    # loc pointe précisément le champ imbriqué
    assert any(err["loc"] == ("primary_address", "postal_code") for err in errors)


def test_reject_extra_field() -> None:
    """Cas 5 : champ inconnu refusé (extra='forbid')."""
    with pytest.raises(ValidationError) as exc_info:
        UserSignup.model_validate(
            {
                "username": "alice_42",
                "email": "alice@example.com",
                "age": 25,
                "password": "longenough123",
                "is_admin": True,  # champ inconnu, attaque potentielle
            }
        )
    errors = exc_info.value.errors()
    assert any(err["type"] == "extra_forbidden" for err in errors)
