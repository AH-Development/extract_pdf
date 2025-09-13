# Image de base
FROM python:3.11-slim

# Répertoire de travail
WORKDIR /app

# Copier et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code
COPY . .

# Exposer le nouveau port
EXPOSE 8885

# Lancer FastAPI sur toutes les interfaces avec le port 8885
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8885"]
