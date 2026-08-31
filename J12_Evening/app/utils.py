# app/utils.py
def apply_discount(price: float, pct: float) -> float:
    return price * (1 - pct / 100)
