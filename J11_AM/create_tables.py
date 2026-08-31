from app.database import Base, engine

Base.metadata.create_all(engine)
print("Tables créées.")
