from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .routers import export, history, rules, upload
from .storage.history_db import init_db

app = FastAPI(title="Analyse BDD Fiches", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(history.router)
app.include_router(rules.router)
app.include_router(export.router)


@app.on_event("startup")
async def startup() -> None:
    init_db()


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


# En production (déploiement), le frontend est buildé (frontend/dist) et servi
# directement par ce même serveur, pour n'avoir qu'un seul site à héberger.
# Cette section est ajoutée APRÈS les routes /api/* pour qu'elles restent prioritaires.
_frontend_dist = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if _frontend_dist.exists():
    app.mount("/", StaticFiles(directory=_frontend_dist, html=True), name="frontend")
