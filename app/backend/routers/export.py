from __future__ import annotations

import io

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from ..core.analyzer import load_cached_dataframe

router = APIRouter(prefix="/api/export", tags=["export"])


@router.get("/{analysis_id}")
async def export_analysis(analysis_id: str, format: str = "csv", statut: str | None = None):
    try:
        df = load_cached_dataframe(analysis_id)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    if statut:
        df = df[df["statut_affichage"] == statut]

    buffer = io.BytesIO()
    if format == "xlsx":
        df.to_excel(buffer, index=False, engine="openpyxl")
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        filename = f"analyse_{analysis_id}.xlsx"
    else:
        df.to_csv(buffer, index=False)
        media_type = "text/csv"
        filename = f"analyse_{analysis_id}.csv"

    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
