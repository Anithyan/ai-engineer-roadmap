def add(a: int, b: int) -> int:
    return a + b


def greet(name: str, formal: bool = False) -> str:
    """Salue une personne."""
    if formal:
        return f"Bonjour, {name}."
    return f"Salut {name} !"


def compute_average(score_sum: float, count: int) -> float:
    """Calcule une moyenne. count doit être > 0 (vérifié au runtime)."""
    if count <= 0:
        raise ValueError("count must be > 0")
    return score_sum / count


# --- Composés ---


def sum_all(numbers: list[int]) -> int:
    """Somme une liste d'entiers."""
    return sum(numbers)


def count_words(text: str) -> dict[str, int]:
    """Compte les occurrences de chaque mot."""
    counts: dict[str, int] = {}
    for word in text.split():
        counts[word] = counts.get(word, 0) + 1
    return counts


def find_user(user_id: int, users: dict[int, str]) -> str | None:
    """Retourne le nom de l'utilisateur ou None s'il n'existe pas."""
    return users.get(user_id)


def parse_age(value: int | str) -> int:
    """Accepte un int ou un str numérique, renvoie un int."""
    if isinstance(value, int):
        return value
    return int(value)  # peut lever ValueError, c'est volontaire
