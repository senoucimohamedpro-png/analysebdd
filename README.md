# Analyse BDD Fiches — Dashboard automatisé

Application web qui remplace le traitement manuel des exports CSV de fiches par une analyse
instantanée : upload, classification, calcul des KPI, dashboard filtrable, historique et export.

## Démarrage rapide (Windows)

Prérequis : Python 3.11+ et Node.js 18+ installés.

```bat
app\start.bat
```

Ce script installe les dépendances (si nécessaire) puis lance :
- le backend FastAPI sur http://127.0.0.1:8000
- le frontend sur http://127.0.0.1:5173 (à ouvrir dans le navigateur)

## Démarrage manuel

```bash
# Backend
cd app
pip install -r backend/requirements.txt
python -m uvicorn backend.main:app --reload --port 8000

# Frontend (autre terminal)
cd app/frontend
npm install
npm run dev
```

## Structure du projet

```
app/
  backend/
    main.py                  # API FastAPI
    core/
      analyzer.py             # orchestration de l'analyse (lecture CSV, KPI, vectorisé pandas)
      classifier.py            # classification positif/traité via rules/classification_rules.yaml
      rules_engine.py          # moteur générique d'évaluation du référentiel IT (blocage)
    rules/
      classification_rules.yaml
      blocking_rules.json      # référentiel IT — modifiable sans toucher au code
    routers/                  # endpoints upload / history / rules / export
    storage/history_db.py     # historique des analyses (SQLite)
  frontend/                  # React + Vite : Upload, Dashboard, Historique, Référentiel/Règles
  data/                      # uploads temporaires, cache parquet par analyse, history.db
  start.bat
```

## Logique métier

- **Classification** (`contact_qualif1`) : positif / traité / non traité — définie dans
  `backend/rules/classification_rules.yaml`.
- **Blocage** : déterminé dynamiquement par le référentiel IT (`backend/rules/blocking_rules.json`),
  basé par défaut sur la sémantique du champ `priorite` documentée par Hermes.Net
  (priorite < 0 = fiche exclue/bloquée selon le code). Modifiable via l'écran "Référentiel / Règles"
  de l'application ou en éditant/réimportant le JSON — aucune règle n'est codée en dur.
- **Fiches actives** = fiches NON bloquées ET NON traitées.

## Contraintes de performance

Le traitement (lecture CSV → classification → blocage → agrégats) est entièrement vectorisé avec
pandas (pas de boucle ligne à ligne), pour tenir l'objectif de 100 000 lignes par fichier en moins
de 30 secondes.
