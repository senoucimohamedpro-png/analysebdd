"""
Orchestration de l'analyse : lecture CSV → classification → blocage → KPI.
Entièrement vectorisé (pandas) pour tenir l'objectif de 100 000 lignes en moins de 30s.
"""
from __future__ import annotations

import time
import uuid
from pathlib import Path

import numpy as np
import pandas as pd

from . import classifier, rules_engine
from ..models.schemas import AnalysisResult, EvolutionPoint, KpiSummary, StatutRepartition

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
CACHE_DIR = DATA_DIR / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

REQUIRED_COLUMNS = [
    "contact_date_fiche",
    "date_chargement",
    "contact_qualif1",
    "code_marketing",
    "nbr_appel",
    "priorite",
]


def _read_csv_files(file_paths: list[Path]) -> pd.DataFrame:
    frames = []
    for path in file_paths:
        df = pd.read_csv(path, dtype=str, keep_default_na=False)
        frames.append(df)
    df = pd.concat(frames, ignore_index=True) if len(frames) > 1 else frames[0]

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Colonnes manquantes dans le CSV: {', '.join(missing)}")

    df["nbr_appel"] = pd.to_numeric(df["nbr_appel"], errors="coerce").fillna(0).astype(int)
    df["priorite"] = pd.to_numeric(df["priorite"], errors="coerce").fillna(0).astype(int)
    return df


def _build_result(df: pd.DataFrame, analysis_id: str, nom_fichier: str, date_analyse: str, duree: float) -> AnalysisResult:
    kpi = KpiSummary(
        total_fiches=int(len(df)),
        fiches_traitees=int(df["est_traite"].sum()),
        fiches_positives=int(df["est_positif"].sum()),
        fiches_non_traitees=int((~df["est_traite"]).sum()),
        fiches_bloquees=int(df["est_bloque"].sum()),
        fiches_actives=int(df["est_actif"].sum()),
    )

    repartition_counts = df["statut_affichage"].value_counts()
    repartition_list = [
        StatutRepartition(statut=str(statut), nombre=int(nombre))
        for statut, nombre in repartition_counts.items()
    ]

    evolution = (
        df.groupby("date_chargement").size().reset_index(name="nombre")
        .sort_values("date_chargement")
    )
    evolution_list = [
        EvolutionPoint(date_chargement=str(row["date_chargement"]), nombre=int(row["nombre"]))
        for _, row in evolution.iterrows()
    ]

    return AnalysisResult(
        analysis_id=analysis_id,
        nom_fichier=nom_fichier,
        date_analyse=date_analyse,
        duree_secondes=duree,
        kpi=kpi,
        repartition_statuts=repartition_list,
        evolution=evolution_list,
        apercu_fiches=df.head(200).to_dict(orient="records"),
        total_lignes_disponibles=int(len(df)),
    )


def run_analysis(file_paths: list[Path], original_names: list[str]) -> AnalysisResult:
    start = time.perf_counter()

    df = _read_csv_files(file_paths)
    df = classifier.classify(df)
    blocking_rules = rules_engine.load_blocking_rules()
    df["est_bloque"] = rules_engine.evaluate_blocking(df, blocking_rules)
    df["est_actif"] = ~df["est_bloque"] & ~df["est_traite"]

    df["statut_affichage"] = np.select(
        [df["est_bloque"], df["est_positif"], df["est_traite"]],
        ["Bloquée", "Positive", "Traitée (autre)"],
        default="Non traitée (active)",
    )

    analysis_id = uuid.uuid4().hex[:12]
    df.to_parquet(CACHE_DIR / f"{analysis_id}.parquet", index=False)
    duree = round(time.perf_counter() - start, 2)

    return _build_result(
        df, analysis_id, ", ".join(original_names),
        pd.Timestamp.now().isoformat(timespec="seconds"), duree,
    )


def load_cached_dataframe(analysis_id: str) -> pd.DataFrame:
    path = CACHE_DIR / f"{analysis_id}.parquet"
    if not path.exists():
        raise FileNotFoundError(f"Analyse {analysis_id} introuvable en cache")
    return pd.read_parquet(path)


def build_summary_from_cache(analysis_id: str, nom_fichier: str, date_analyse: str, duree_secondes: float) -> AnalysisResult:
    df = load_cached_dataframe(analysis_id)
    return _build_result(df, analysis_id, nom_fichier, date_analyse, duree_secondes)
