Backend FastAPI (MySQL Edition)
===============================

Ce dépôt contient le backend de votre application, développé avec FastAPI et SQLAlchemy (async) pour une base MySQL (`mysql+aiomysql`).

Prérequis
---------

-   Python 3.10+
-   MySQL (local ou distant)
-   Docker (pour la conteneurisation)
-   k3d/k3s + kubectl (pour déploiement eventual)

Installation locale
-------------------

### 1\. Cloner le projet

bash

```
git clone <votre-repo-url>
cd backend
```

### 2\. Créer et activer l'environnement virtuel

bash

```
python3 -m venv .venv
source .venv/bin/activate
```

### 3\. Installer les dépendances

bash

```
pip install --upgrade pip
pip install -r requirements.txt
```

### 4\. Configuration

Créez un fichier `.env` à la racine avec :

env

```
DATABASE_URL=mysql+aiomysql://<USER>:<PASSWORD>@<HOST>:<PORT>/<DB_NAME>
JWT_SECRET=votre_clef_secrete_pour_jwt
FAAS_GATEWAY=http://127.0.0.1:31112
FAAS_USER=<openfaas_user>
FAAS_PASS=<openfaas_password>
```

### 5\. Démarrer MySQL

Exemple avec Docker :

bash

```
docker run -d --name mysql-local\
  -e MYSQL_ROOT_PASSWORD=secret\
  -e MYSQL_DATABASE=<DB_NAME>\
  -e MYSQL_USER=<USER>\
  -e MYSQL_PASSWORD=<PASSWORD>\
  -p 3306:3306 mysql:8
```

### 6\. Lancer l'application

bash

```
uvicorn app.main:app --reload
```
ou en debug mode
```
uvicorn app.main:app --reload --log-level debug

```

L'API est disponible sur <http://127.0.0.1:8000>.

Endpoints principaux
--------------------


- `GET  http://127.0.0.1:8000/health`  
  Vérifie que le service est en ligne.

- `POST http://127.0.0.1:8000/signup`  
  Création de compte (paramètre JSON : `{ "username": "…"} →` renvoie un mot de passe + QR code TOTP).
   **Exemple :**
    ```bash
    curl -i -X POST http://127.0.0.1:8000/signup \
      -H "Content-Type: application/json" \
      -d '{"username":"Enzo"}'

- `POST http://127.0.0.1:8000/login`  
  Authentification (JSON : `{ "username": "…", "password": "…", "totp_code": "…" }` → JWT + profil).
    **Exemple :**
    ```bash
    curl -i -X POST http://127.0.0.1:8000/login \
    -H "Content-Type: application/json" \
    -d '{"username": "Enzo",
        "password": "pjaTgIVC7yiQ",
        "totp_code": "114857"}'

- `GET  http://127.0.0.1:8000/users/me`  
  Récupère le profil de l’utilisateur (JWT dans l’en-tête `Authorization: Bearer <token>` requis).

- `GET  http://127.0.0.1:8000/users/`  
  Liste tous les utilisateurs (JWT requis).

Docker
------

### Construire l'image

bash

```
docker build -t backend:latest .
```

### Lancer le conteneur

bash

```
docker run --rm -p 8000:8000 --env-file .env backend:latest
```

Docker Compose (optionnel)
--------------------------

yaml

```
version: '3.8'
services:
  db:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: secret
      MYSQL_DATABASE: ${DB_NAME}
      MYSQL_USER: ${USER}
      MYSQL_PASSWORD: ${PASSWORD}
    ports:
      - "3306:3306"

  api:
    build: .
    depends_on:
      - db
    env_file: .env
    ports:
      - "8000:8000"
```

bash

```
docker-compose up --build
```

Tests
-----

bash

```
pytest --maxfail=1 --disable-warnings -q
```

Déploiement Kubernetes
----------------------

1.  Construisez et poussez votre image sur un registry accessible.
2.  Appliquez vos manifests dans `k8s/` :

bash

```
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/backend-deployment.yaml
```

1.  Vérifiez les pods et services :

bash

```
kubectl get pods,svc -n default
```

test 
```
pytest -q
```
