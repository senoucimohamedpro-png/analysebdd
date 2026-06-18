"""
Classification des fiches selon contact_qualif1 (rules/classification_rules.yaml).
Aucune valeur métier en dur ici : tout vient du fichier YAML, modifiable sans déploiement.
"""
from __future__ import annotations

import unicodedata
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

RULES_DIR = Path(__file__).resolve().parent.parent / "rules"
CLASSIFICATION_RULES_PATH = RULES_DIR / "classification_rules.yaml"


def _normalize(value: str) -> str:
    if not isinstance(value, str):
        return ""
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return value.strip().lower()


def load_classification_rules(path: Path = CLASSIFICATION_RULES_PATH) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_classification_rules(data: dict[str, Any], path: Path = CLASSIFICATION_RULES_PATH) -> None:
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def classify(df: pd.DataFrame, rules_config: dict[str, Any] | None = None) -> pd.DataFrame:
    """Ajoute les colonnes 'est_positif' et 'est_traite' au DataFrame (vectorisé)."""
    rules_config = rules_config or load_classification_rules()
    positif_set = {_normalize(v) for v in rules_config.get("positif", [])}
    traite_set = {_normalize(v) for v in rules_config.get("traite", [])}

    qualif_norm = df["contact_qualif1"].map(_normalize)
    df = df.copy()
    df["est_positif"] = qualif_norm.isin(positif_set)
    df["est_traite"] = qualif_norm.isin(traite_set)
    return df
