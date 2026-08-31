"""Bloc 7 : nested models — User qui contient Address."""

from pydantic import BaseModel, ConfigDict, EmailStr, Field, ValidationError


class Address(BaseModel):
    """Adresse postale française."""

    model_config = ConfigDict(extra="forbid")
    street: str = Field(min_length=1, max_length=200)
    city: str = Field(min_length=1, max_length=100)
    postal_code: str = Field(pattern=r"^\d{5}$")  # 5 chiffres exactement
    country: str = Field(default="France", min_length=2, max_length=50)


class User(BaseModel):
    """Utilisateur avec adresse imbriquée + liste d'adresses secondaires."""

    model_config = ConfigDict(extra="forbid")

    user_id: int = Field(gt=0)
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=120)
    primary_address: Address  # nested obligatoire
    secondary_addresses: list[Address] = Field(
        default_factory=list
    )  # nested liste, défaut [] safe


def demo_valid() -> None:
    """User construit depuis un dict (style API JSON)."""
    payload = {
        "user_id": 1,
        "name": "Alice Martin",
        "email": "alice@example.com",
        "age": 30,
        "primary_address": {
            "street": "12 rue de la Paix",
            "city": "Paris",
            "postal_code": "75002",
        },
        "secondary_addresses": [
            {
                "street": "5 avenue Foch",
                "city": "Lyon",
                "postal_code": "69006",
                "country": "France",
            }
        ],
    }
    user = User.model_validate(payload)
    print(user)
    print(f"User créé : {user.name}")
    print(
        f"  Adresse principale : {user.primary_address.city} ({user.primary_address.postal_code})"  # noqa : E501
    )
    print(f"  Adresses secondaires : {len(user.secondary_addresses)}")


def demo_invalid_nested() -> None:
    """Erreur sur le nested model : code postal invalide."""
    payload = {
        "user_id": 1,
        "name": "Bob",
        "email": "alice@example.com",
        "age": 25,
        "primary_address": {
            "street": "1 rue X",
            "city": "Paris",
            "postal_code": "ABCDE",  # ne matche pas ^\d{5}$
        },
    }
    try:
        User.model_validate(payload)
    except ValidationError as e:
        print("Erreur dans le nested model :")
        for err in e.errors():
            print(f"  - {'.'.join(str(x) for x in err['loc'])}: {err['msg']}")


if __name__ == "__main__":
    demo_valid()
    print("---")
    demo_invalid_nested()
