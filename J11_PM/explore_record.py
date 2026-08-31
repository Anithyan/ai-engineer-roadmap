# explore_record.py  (fichier de test jetable)
import logging


# on capture le record au lieu de l'afficher formaté
class PeekFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        print("===== TOUS LES ATTRIBUTS DU RECORD =====")
        for key, value in record.__dict__.items():
            print(f"  {key!r:20} = {value!r}")
        print("========================================")
        return super().format(record)  # affiche aussi le log normalement


handler = logging.StreamHandler()
handler.setFormatter(PeekFormatter())
logging.basicConfig(level=logging.INFO, handlers=[handler], force=True)

log = logging.getLogger("app")
log.info(
    "user logged in", extra={"user_id": 42}
)  # un extra pour bien voir la différence
