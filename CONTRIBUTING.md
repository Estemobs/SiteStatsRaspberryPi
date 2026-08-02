# Contribution

Merci de vouloir contribuer à SiteStatsRaspberryPi !

## Développement

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # puis éditez .env
```

## Lancement

```bash
python transfert_valeur.py        # serveur FastAPI (dashboard)
python mesure_valeur.py           # collecte locale
python mesure_valeur_vps.py       # collecte distante
```

## Vérifications avant PR

```bash
python -m compileall -q .
```

## Pull requests

1. Décrivez le problème résolu et testez en local.
2. Gardez la PR petite et ciblée.
3. Référencez l'issue concernée dans la description.

## Licence

Ce projet est sous licence MIT.
