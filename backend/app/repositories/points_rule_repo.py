from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.points_rule import PointsRule


class PointsRuleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(
        self, season_id: int | None = None, rule_type: str | None = None
    ) -> list[PointsRule]:
        query = select(PointsRule)
        if season_id:
            query = query.where(PointsRule.season_id == season_id)
        if rule_type:
            query = query.where(PointsRule.rule_type == rule_type)
        result = await self.db.execute(query.order_by(PointsRule.id))
        return list(result.scalars().all())

    async def get_by_id(self, rule_id: int) -> PointsRule | None:
        result = await self.db.execute(select(PointsRule).where(PointsRule.id == rule_id))
        return result.scalar_one_or_none()

    async def find_duplicate(
        self, season_id: int, rule_type: str, event_level: str | None,
        group_name: str | None, result_type: str | None, exclude_id: int | None = None,
    ) -> PointsRule | None:
        query = select(PointsRule).where(
            PointsRule.season_id == season_id,
            PointsRule.rule_type == rule_type,
        )
        if event_level is None:
            query = query.where(PointsRule.event_level.is_(None))
        else:
            query = query.where(PointsRule.event_level == event_level)
        if group_name is None:
            query = query.where(PointsRule.group_name.is_(None))
        else:
            query = query.where(PointsRule.group_name == group_name)
        if result_type is None:
            query = query.where(PointsRule.result_type.is_(None))
        else:
            query = query.where(PointsRule.result_type == result_type)
        if exclude_id:
            query = query.where(PointsRule.id != exclude_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, **kwargs) -> PointsRule:
        rule = PointsRule(**kwargs)
        self.db.add(rule)
        await self.db.flush()
        return rule

    async def update(self, rule: PointsRule, **kwargs) -> PointsRule:
        for key, value in kwargs.items():
            if value is not None:
                setattr(rule, key, value)
        await self.db.flush()
        return rule

    async def delete(self, rule: PointsRule) -> None:
        await self.db.delete(rule)
        await self.db.flush()
