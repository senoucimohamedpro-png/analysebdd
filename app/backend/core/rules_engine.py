"""
Moteur de règles générique.

Toute la logique de "qu'est-ce qui bloque une fiche" est ici pilotée par des données
(rules/blocking_rules.json), jamais par du code en dur. On peut ajouter/modifier/supprimer
une règle sans toucher à ce fichier.
"""
from __future__ import annotations

import json
import operator
from pathlib import Path
from typing import Any

import pandas as pd

RULES_DIR = Path(__file__).resolve().parent.parent / "rules"
BLOCKING_RULES_PATH = RULES_DIR / "blocking_rules.json"

_OPERATORS = {
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le,
    "in": lambda s, v: s.isin(v),
    "not_in": lambda s, v: ~s.isin(v),
    "between": lambda s, v: s.between(v[0], v[1]),
}


def load_blocking_rules(path: Path = BLOCKING_RULES_PATH) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_blocking_rules(data: dict[str, Any], path: Path = BLOCKING_RULES_PATH) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def evaluate_blocking(df: pd.DataFrame, rules_config: dict[str, Any] | None = None) -> pd.Series:
    """Retourne un booléen par ligne: True si la fiche est bloquée, selon le référentiel IT."""
    rules_config = rules_config or load_blocking_rules()
    blocked = pd.Series(False, index=df.index)
    exception = pd.Series(False, index=df.index)

    for rule in rules_config.get("regles", []):
        champ = rule["champ"]
        if champ not in df.columns:
            continue
        op_fn = _OPERATORS.get(rule["operateur"])
        if op_fn is None:
            continue
        try:
            mask = op_fn(df[champ], rule["valeur"])
        except Exception:
            continue
        if rule.get("bloque", True):
            blocked = blocked | mask
        else:
            # règle non-bloquante explicite : exclut ces lignes du blocage même si une autre règle matche
            exception = exception | mask

    return blocked & ~exception
