# ---- Étape 1 : Builder ----
    FROM python:3.10-slim AS builder

    # Installer paquets de compilation et client MySQL
    RUN apt-get update \
     && apt-get install -y --no-install-recommends \
          build-essential \
          default-libmysqlclient-dev \
     && rm -rf /var/lib/apt/lists/*
    
    WORKDIR /app
    
    # Copier et installer les dépendances
    COPY requirements.txt .
    RUN pip install --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt
    
    # Copier le code
    COPY app/ ./app
    
    # ---- Étape 2 : Image finale ----
    FROM python:3.10-slim
    
    # Installer runtime client MySQL
    RUN apt-get update \
     && apt-get install -y --no-install-recommends \
          default-libmysqlclient-dev \
     && rm -rf /var/lib/apt/lists/*
    
    WORKDIR /app
    
    # Copier les packages Python du builder
    COPY --from=builder /usr/local/lib/python3.10/site-packages \
                       /usr/local/lib/python3.10/site-packages
    
    # Copier le code applicatif
    COPY app/ ./app
    
    # Exposer le port
    EXPOSE 8000
    
    # Variables d’environnement
    ENV PYTHONUNBUFFERED=1 \
        PYTHONDONTWRITEBYTECODE=1 \
        UVICORN_WORKERS=2
    
    # Commande de démarrage
    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "${UVICORN_WORKERS}"]