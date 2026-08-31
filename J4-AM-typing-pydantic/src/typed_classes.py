"""Bloc 4 : classes Python typées (PAS encore Pydantic — vient au Bloc 5)."""


class Product:
    """Représente un produit dans un catalogue (classe Python pure)."""

    # Annotations d'attributs au niveau classe
    name: str
    price: float
    in_stock: bool
    tags: list[str]

    def __init__(
        self,
        name: str,
        price: float,
        in_stock: bool = True,
        tags: list[str] | None = None,  # ← pattern anti-piège du défaut mutable
    ) -> None:
        self.name = name
        self.price = price
        self.in_stock = in_stock
        self.tags = (
            tags if tags is not None else []
        )  # ← création locale à chaque instance

    def apply_discount(self, percent: float) -> float:
        """Renvoie le prix après remise (sans modifier self.price)."""
        return self.price * (1 - percent / 100)

    def add_tag(self, tag: str) -> None:
        """Ajoute un tag (modifie self.tags en place)."""
        self.tags.append(tag)


class Cart:
    """Panier qui contient une liste de Product."""

    items: list[Product]

    def __init__(self) -> None:
        self.items = []

    def add(self, product: Product) -> None:
        self.items.append(product)

    def total(self) -> float:
        return sum(p.price for p in self.items if p.in_stock)
