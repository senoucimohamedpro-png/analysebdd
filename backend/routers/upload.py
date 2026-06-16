from __future__ import annotations

import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile

from ..core.analyzer import run_analysis
from ..models.schemas import AnalysisResult
from ..storage import history_db

router = APIRouter(prefix="/api/upload", tags=["upload"])

UPLOAD_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("", response_model=AnalysisResult)
async def upload_csv(files: list[UploadFile]) -> AnalysisResult:
    if not files:
        raise HTTPException(status_code=400, detail="Aucun fichier fourni")

    saved_paths: list[Path] = []
    original_names: list[str] = []
    try:
        for f in files:
            if not f.filename.lower().endswith(".csv"):
                raise HTTPException(status_code=400, detail=f"Fichier non CSV refusé: {f.filename}")
            dest = UPLOAD_DIR / f"{uuid.uuid4().hex[:8]}_{f.filename}"
            with open(dest, "wb") as out:
                shutil.copyfileobj(f.file, out)
            saved_paths.append(dest)
            original_names.append(f.filename)

        result = run_analysis(saved_paths, original_names)
        history_db.save_result(result)
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    finally:
        for p in saved_paths:
            p.unlink(missing_ok=True)
