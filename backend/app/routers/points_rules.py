from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.schemas.points_rule import PointsRuleCreate, PointsRuleUpdate
from app.services.points_rule_service import PointsRuleService

router = APIRouter(prefix="/api/v1/admin/points-rules", tags=["points-rules"])


@router.get("", response_model=None)
async def list_rules(
    season_id: int | None = None,
    rule_type: str | None = None,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = PointsRuleService(db)
    rules = await service.list_rules(season_id, rule_type)
    return {
        "data": [
            {
                "id": r.id,
                "season_id": r.season_id,
                "rule_type": r.rule_type,
                "event_level": r.event_level,
                "group_name": r.group_name,
                "result_type": r.result_type,
                "points": r.points,
                "enabled": r.enabled,
            }
            for r in rules
        ],
    }


@router.post("", response_model=None, status_code=201)
async def create_rule(
    body: PointsRuleCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = PointsRuleService(db)
    rule = await service.create_rule(body)
    return {
        "data": {
            "id": rule.id,
            "season_id": rule.season_id,
            "rule_type": rule.rule_type,
            "event_level": rule.event_level,
            "group_name": rule.group_name,
            "result_type": rule.result_type,
            "points": rule.points,
            "enabled": rule.enabled,
        },
        "message": "ok",
    }


@router.put("/{rule_id}", response_model=None)
async def update_rule(
    rule_id: int,
    body: PointsRuleUpdate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = PointsRuleService(db)
    rule = await service.update_rule(rule_id, body)
    return {
        "data": {
            "id": rule.id,
            "season_id": rule.season_id,
            "rule_type": rule.rule_type,
            "event_level": rule.event_level,
            "group_name": rule.group_name,
            "result_type": rule.result_type,
            "points": rule.points,
            "enabled": rule.enabled,
        },
        "message": "ok",
    }


@router.delete("/{rule_id}", response_model=None)
async def delete_rule(
    rule_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = PointsRuleService(db)
    await service.delete_rule(rule_id)
    return {"message": "ok"}
