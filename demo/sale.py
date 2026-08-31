import json
from pathlib import Path


def charge_commandes(chemin):
    donnees = json.loads(Path(chemin).read_text())
    total = 0
    #    debug_flag = 42
    for element in donnees["items"]:
        total += element["prix"]
    print(
        "Le total des commandes calculé pour ce fichier de démonstration vaut :", total
    )
    return total
