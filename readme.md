# Système de Surveillance Raspberry Pi

Ce dépôt permet de surveiller les performances d'un Raspberry Pi 4 via une interface web.

![Dashboard](img/screenshot.png)

## Architecture

- **db.py** : accès à la base **SQLite** partagée (table `data`), utilisée par le serveur web et par `mesure_valeur.py` en local.
- **config.py** : charge la configuration depuis un fichier `.env` (aucun identifiant en dur dans le code).
- **transfert_valeur.py** : serveur web **FastAPI** (remplace l'ancien serveur Tornado/MySQL). Il sert :
  - `GET /` : le tableau de bord (`adminPI.html`), rempli avec la dernière mesure enregistrée en SQLite.
  - `POST /api/measurements` : point d'entrée d'ingestion, protégé par un jeton `Bearer` (`API_TOKEN`), utilisé par les sources de mesure distantes.
- **mesure_valeur.py** : à exécuter **sur la même machine** que le serveur (ex. le Raspberry Pi lui-même). Écrit directement dans le fichier SQLite via `db.py`.
- **mesure_valeur_vps.py** : à exécuter sur une **machine distante**. Envoie ses mesures au serveur via une requête HTTP `POST /api/measurements` authentifiée par jeton — il n'a donc pas besoin d'accès direct à la base de données.
- **adminPI.html** : template Jinja2 affiché par FastAPI.
- **requirements.txt** : dépendances (FastAPI, uvicorn, python-dotenv, requests, psutil).

## Configuration (.env)

Aucun secret n'est stocké dans le code. Copiez `.env.example` en `.env` et renseignez vos valeurs :

```bash
cp .env.example .env
```

```
DB_PATH=data.db
API_HOST=0.0.0.0
API_PORT=2006
API_TOKEN=            # générez-en un: python -c "import secrets; print(secrets.token_hex(32))"
API_URL=http://localhost:2006/api/measurements
PING_TARGET=google.com
```

`.env` est ignoré par git (voir `.gitignore`) et ne doit jamais être commité.

- Sur la machine qui héberge le serveur **et** `mesure_valeur.py` : renseignez `DB_PATH` et `API_TOKEN`.
- Sur une machine distante qui exécute `mesure_valeur_vps.py` : renseignez `API_URL` (adresse publique du serveur) et le même `API_TOKEN` que le serveur.

## Instructions pour lancer le site

1. **Clonez le dépôt** :
   ```bash
   git clone https://github.com/Estemobs/SiteStatsRaspberryPi.git
   ```

2. **Installez les dépendances** :
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configurez `.env`** (voir section ci-dessus).

4. **Lancez le serveur web** (crée aussi la base SQLite si besoin) :
   ```bash
   python transfert_valeur.py
   ```

5. **Collectez des données** :
   - **Depuis le Raspberry Pi / la machine du serveur** :
     ```bash
     python mesure_valeur.py
     ```
   - **Depuis un serveur distant** :
     ```bash
     python mesure_valeur_vps.py
     ```

6. **Accédez à l'interface utilisateur** dans votre navigateur à l'adresse :
   ```
   http://localhost:2006
   ```

## Note

Planifiez `mesure_valeur.py` (ou `mesure_valeur_vps.py`) via une tâche cron pour une mise à jour périodique des mesures.
