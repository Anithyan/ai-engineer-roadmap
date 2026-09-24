# ---------- Stage 1 : builder (installe les dépendances) ----------
FROM python:3.12-slim AS builder

WORKDIR /app

# On installe les deps dans un dossier isolé (/install) qu'on copiera ensuite
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---------- Stage 2 : image finale (légère) ----------
FROM python:3.12-slim

WORKDIR /app

# Récupère UNIQUEMENT les paquets installés au stage builder
COPY --from=builder /install /usr/local

# Copie ton code applicatif
COPY . .

# Le port sur lequel uvicorn écoutera
EXPOSE 8080

# Lance l'app. --host 0.0.0.0 = écoute hors du conteneur (obligatoire en conteneur)
CMD ["sh","-c","exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
