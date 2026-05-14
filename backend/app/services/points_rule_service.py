from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BusinessConflictError, NotFoundError
from app.repositories.entries_points_repo import EntriesPointsRepository
from app.repositories.points_rule_repo import PointsRuleRepository
from app.repositories.season_repo import SeasonRepository
from app.schemas.points_rule import PointsRuleCreate, PointsRuleUpdate


class PointsRuleService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = PointsRuleRepository(db)
        self.season_repo = SeasonRepository(db)
        self.entries_repo = EntriesPointsRepository(db)

    async def list_rules(self, season_id: int | None = None, rule_type: str | None = None):
        if season_id is None:
            active = await self.season_repo.get_active()
            if active:
                season_id = active.id
        return await self.repo.list(season_id, rule_type)

    async def create_rule(self, data: PointsRuleCreate):
        active = await self.season_repo.get_active()
        if not active:
            raise BusinessConflictError(
                detail="无激活赛季，无法创建规则", code="TOURNAMENT_NO_ACTIVE_SEASON"
            )

        duplicate = await self.repo.find_duplicate(
            season_id=active.id,
            rule_type=data.rule_type,
            event_level=data.event_level,
            group_name=data.group_name,
            result_type=data.result_type,
        )
        if duplicate:
            raise BusinessConflictError(detail="该规则组合已存在", code="RULE_DUPLICATE")

        rule = await self.repo.create(season_id=active.id, **data.model_dump())
        await self.db.commit()
        return rule

    async def update_rule(self, rule_id: int, data: PointsRuleUpdate):
        rule = await self.repo.get_by_id(rule_id)
        if not rule:
            raise NotFoundError(detail="规则不存在", code="RULE_NOT_FOUND")

        update_data = data.model_dump(exclude_unset=True)
        rule = await self.repo.update(rule, **update_data)
        await self.db.commit()
        return rule

    async def delete_rule(self, rule_id: int):
        rule = await self.repo.get_by_id(rule_id)
        if not rule:
            raise NotFoundError(detail="规则不存在", code="RULE_NOT_FOUND")

        await self.repo.delete(rule)
        await self.db.commit()
