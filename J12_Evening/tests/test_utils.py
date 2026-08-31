# tests/test_utils.py
from app.utils import apply_discount


def test_discount_INUTILE():
    apply_discount(100, 10)  # la ligne s'exécute → couverte
    assert True  # ne vérifie RIEN → 100% de couverture, 0 preuve


def test_discount_VRAI():
    assert apply_discount(100, 10) == 90.0  # vérifie vraiment le comportement
