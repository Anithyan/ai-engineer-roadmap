# syntax=docker/dockerfile:1

# ---- Étape 1 : builder (installe les dépendances dans un venv) ----
FROM python:3.12-slim AS builder
WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Étape 2 : runtime (image finale, ne contient que le venv + le code) ----
FROM python:3.12-slim
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
COPY . .
CMD ["python", "main.py"]
