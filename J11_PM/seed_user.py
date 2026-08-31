# scripts/seed_user.py
from app.core.security import hash_password
from app.database import SessionLocal
from app.models import User
from sqlalchemy import select


def main():
    db = SessionLocal()
    if db.scalar(select(User).where(User.email == "johndoe@example.com")) is None:
        db.add(
            User(email="johndoe@example.com", hashed_password=hash_password("secret"))
        )
        db.commit()
        print("user créé -> johndoe@example.com / secret")
    else:
        print("user déjà présent")
    db.close()


if __name__ == "__main__":
    main()
