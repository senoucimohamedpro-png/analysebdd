"""Historique des analyses, persisté en SQLite local (data/history.db)."""
from __future__ import annotations

import sqlite3
from pathlib import Path

from ..models.schemas import AnalysisResult, HistoryEntry

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
DB_PATH = DATA_DIR / "history.db"


def init_db() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS analyses (
                analysis_id TEXT PRIMARY KEY,
                nom_fichier TEXT,
                date_analyse TEXT,
                duree_secondes REAL,
                total_fiches INTEGER,
                fiches_traitees INTEGER,
                fiches_positives INTEGER,
                fiches_non_traitees INTEGER,
                fiches_bloquees INTEGER,
                fiches_actives INTEGER
            )
            """
        )


def save_result(result: AnalysisResult) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO analyses (
                analysis_id, nom_fichier, date_analyse, duree_secondes,
                total_fiches, fiches_traitees, fiches_positives,
                fiches_non_traitees, fiches_bloquees, fiches_actives
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                result.analysis_id,
                result.nom_fichier,
                result.date_analyse,
                result.duree_secondes,
                result.kpi.total_fiches,
                result.kpi.fiches_traitees,
                result.kpi.fiches_positives,
                result.kpi.fiches_non_traitees,
                result.kpi.fiches_bloquees,
                result.kpi.fiches_actives,
            ),
        )


def list_history() -> list[HistoryEntry]:
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            """
            SELECT analysis_id, nom_fichier, date_analyse, duree_secondes,
                   total_fiches, fiches_actives, fiches_bloquees
            FROM analyses ORDER BY date_analyse DESC
            """
        ).fetchall()
    return [
        HistoryEntry(
            analysis_id=r[0],
            nom_fichier=r[1],
            date_analyse=r[2],
            duree_secondes=r[3],
            total_fiches=r[4],
            fiches_actives=r[5],
            fiches_bloquees=r[6],
        )
        for r in rows
    ]
