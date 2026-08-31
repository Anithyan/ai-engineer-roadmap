# IMPORT v2 : depuis "pydantic_settings" (underscore), PAS depuis "pydantic".
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # model_config = comment BaseSettings se comporte :
    #   env_file=".env" -> lis les valeurs dans .env (à la racine)
    #   extra="ignore"  -> tolère une clé du .env non déclarée ici (sans planter)
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Sans valeur par défaut = REQUIS. Doit venir du .env, sinon crash au démarrage.
    DATABASE_URL: str
    SECRET_KEY: str

    # Avec valeur par défaut = optionnel (mêmes valeurs que ton security.py actuel).
    ALGORITHM: str = "HS256"
    # Typé "int" : la string "30" du .env serait convertie en entier.
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


# UNE seule instance, importée partout ailleurs via "from app.core.config import settings".
settings = Settings()
