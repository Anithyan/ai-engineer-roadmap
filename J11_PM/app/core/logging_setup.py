# app/core/logging_setup.py  (NOUVEAU)
import json
import logging
from datetime import datetime, timezone

# Attributs "standard" d'un LogRecord -> sert à repérer mes champs perso (extra=)
_RESERVED = set(vars(logging.makeLogRecord({})).keys())


class JsonFormatter(logging.Formatter):
    # J'hérite de Formatter et je redéfinis format() : je renvoie du JSON, pas du texte.
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            # record.created = heure (epoch) -> ISO lisible + UTC
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).isoformat(),
            "level": record.levelname,  # "INFO", "ERROR"...
            "logger": record.name,
            "message": record.getMessage(),  # le message final
        }
        # ajoute les champs passés via extra={...}
        for key, value in record.__dict__.items():
            if key not in _RESERVED:
                payload[key] = value
        # si exception (log.error(..., exc_info=True)) -> ajoute la traceback
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        # UNE ligne JSON ; ensure_ascii=False garde les accents lisibles
        return json.dumps(payload, ensure_ascii=False)


def setup_logging(level: int = logging.INFO) -> None:
    handler = logging.StreamHandler()  # écrit sur la console
    handler.setFormatter(JsonFormatter())  # branche MON formatter JSON
    # force=True -> remplace toute config de log déjà en place (évite les doublons)
    logging.basicConfig(level=level, handlers=[handler], force=True)
