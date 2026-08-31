"""Bloc 6 : contraintes métier avec Field()."""

from pydantic import BaseModel, ConfigDict, EmailStr, Field, ValidationError


class UserSignup(BaseModel):
    """Modèle d'inscription utilisateur, avec contraintes métier strictes."""

    # extra='forbid' : refuser tout champ inconnu (sinon Pydantic les ignore par défaut)
    model_config = ConfigDict(extra="forbid")

    username: str = Field(min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr  # validation format email built-in
    age: int = Field(ge=13, le=120)  # âge entre 13 et 120 inclus
    password: str = Field(min_length=8, max_length=128)
    bio: str | None = Field(default=None, max_length=500)  # optionnel, max 500 chars
    score: float = Field(default=0.0, ge=0.0, le=100.0)  # score initial 0, 0-100


def demo() -> None:
    # Cas valide
    u = UserSignup(
        username="alice_42",
        email="alice@example.com",  # ← email factice valide
        age=28,
        password="hunter2_strong",
    )
    print(f"Valide: {u.model_dump()}")

    # Cas invalide : 6 erreurs à la fois (Pydantic les remonte toutes [B])
    invalid_payload = {
        "username": "ab",  # trop court (min_length=3)
        "email": "pas-un-email",  # format invalide
        "age": 200,  # > 120
        "password": "court",  # trop court (min_length=8)
        "bio": "x" * 600,  # > 500 chars
        "champ_inconnu": "boum",  # extra='forbid'
    }
    try:
        UserSignup.model_validate(invalid_payload)
    except ValidationError as e:
        print(f"\n{len(e.errors())} erreurs détectées :")
        for err in e.errors():
            loc = ".".join(str(x) for x in err["loc"])
            print(f"  - {loc}: {err['msg']}")


if __name__ == "__main__":
    demo()
