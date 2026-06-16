from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from ..core import classifier, rules_engine

router = APIRouter(prefix="/api/rules", tags=["rules"])


@router.get("/blocking")
async def get_blocking_rules() -> dict[str, Any]:
    return rules_engine.load_blocking_rules()


@router.put("/blocking")
async def update_blocking_rules(rules: dict[str, Any]) -> dict[str, Any]:
    rules_engine.save_blocking_rules(rules)
    return rules


@router.get("/classification")
async def get_classification_rules() -> dict[str, Any]:
    return classifier.load_classification_rules()


@router.put("/classification")
async def update_classification_rules(rules: dict[str, Any]) -> dict[str, Any]:
    classifier.save_classification_rules(rules)
    return rules
