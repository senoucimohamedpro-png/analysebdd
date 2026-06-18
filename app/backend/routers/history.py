from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..core.analyzer import build_summary_from_cache, load_cached_dataframe
from ..models.schemas import AnalysisResult, HistoryEntry
from ..storage import history_db

router = APIRouter(prefix="/api/history", tags=["history"])


@router.get("", response_model=list[HistoryEntry])
async def get_history() -> list[HistoryEntry]:
    return history_db.list_history()


@router.get("/{analysis_id}/summary", response_model=AnalysisResult)
async def get_summary(analysis_id: str) -> AnalysisResult:
    entry = next((h for h in history_db.list_history() if h.analysis_id == analysis_id), None)
    if entry is None:
        raise HTTPException(status_code=404, detail="Analyse introuvable")
    try:
        return build_summary_from_cache(analysis_id, entry.nom_fichier, entry.date_analyse, entry.duree_secondes)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{analysis_id}/filtres")
async def get_filtres(analysis_id: str):
    try:
        df = load_cached_dataframe(analysis_id)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {
        "dates_chargement": sorted(df["date_chargement"].dropna().unique().tolist()),
        "codes_marketing": sorted(df["code_marketing"].dropna().unique().tolist()),
    }


@router.get("/{analysis_id}/fiches")
async def get_fiches(
    analysis_id: str,
    statut: str | None = None,
    code_marketing: str | None = None,
    date_chargement: str | None = None,
    limit: int = 500,
    offset: int = 0,
):
    try:
        df = load_cached_dataframe(analysis_id)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    if statut:
        df = df[df["statut_affichage"] == statut]
    if code_marketing:
        df = df[df["code_marketing"] == code_marketing]
    if date_chargement:
        df = df[df["date_chargement"] == date_chargement]

    total = len(df)
    page = df.iloc[offset: offset + limit]
    return {"total": total, "fiches": page.to_dict(orient="records")}
