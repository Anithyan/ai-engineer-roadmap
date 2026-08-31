"""Bloc 5 : Pydantic BaseModel — validation à l'instanciation."""

from datetime import datetime

from pydantic import BaseModel, ValidationError


class Article(BaseModel):
    """Un article de blog basique."""

    title: str
    content: str
    author_id: int
    published: bool = False
    created_at: datetime | None = None


def demo_valid() -> None:
    """Cas qui marche : tous les champs requis sont fournis."""
    a = Article(
        title="Mon premier post",
        content="Hello world",
        author_id=42,
    )
    print(f"OK: {a}")
    print(f"Serialise: {a.model_dump()}")
    print(f"JSON     : {a.model_dump_json()}")


def demo_coercion() -> None:
    """Pydantic peut convertir : '42' (str) -> 42 (int)."""
    a = Article(
        title="Coercion",
        content="...",
        author_id="42",
    )
    print(
        f"author_id recu '42' (str), stocke {a.author_id} (type {type(a.author_id).__name__})"  # noqa : E501
    )


def demo_invalid() -> None:
    """Cas qui plante : type incompatible."""
    try:
        Article(
            title="Test",
            content="...",
            author_id="pas un nombre",
        )
    except ValidationError as e:
        print("ValidationError attrapee :")
        print(e)


if __name__ == "__main__":
    demo_valid()
    print("---")
    demo_coercion()
    print("---")
    demo_invalid()
