from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class KpiSummary(BaseModel):
    total_fiches: int
    fiches_traitees: int
    fiches_positives: int
    fiches_non_traitees: int
    fiches_bloquees: int
    fiches_actives: int


class StatutRepartition(BaseModel):
    statut: str
    nombre: int


class EvolutionPoint(BaseModel):
    date_chargement: str
    nombre: int


class AnalysisResult(BaseModel):
    analysis_id: str
    nom_fichier: str
    date_analyse: str
    duree_secondes: float
    kpi: KpiSummary
    repartition_statuts: list[StatutRepartition]
    evolution: list[EvolutionPoint]
    apercu_fiches: list[dict[str, Any]]
    total_lignes_disponibles: int


class HistoryEntry(BaseModel):
    analysis_id: str
    nom_fichier: str
    date_analyse: str
    duree_secondes: float
    total_fiches: int
    fiches_actives: int
    fiches_bloquees: int
