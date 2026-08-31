# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

# load_dotenv()  # lit .env et remplit les variables d'environnement

DATABASE_URL = settings.DATABASE_URL

# echo=True affiche le SQL généré dans la console (pratique pour apprendre)
engine = create_engine(DATABASE_URL, echo=True)  # [B]

# fabrique de sessions : chaque appel SessionLocal() crée une nouvelle session
SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):  # [B] classe-mère de tous tes modèles
    pass


# à ajouter à la fin de app/database.py
def get_db():
    db = SessionLocal()
    try:
        yield db  # FastAPI récupère la session ici
    finally:
        db.close()  # fermée après la réponse, même en cas d'erreur
