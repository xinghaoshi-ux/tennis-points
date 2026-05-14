from pydantic import BaseModel


class PointsRuleCreate(BaseModel):
    rule_type: str
    event_level: str | None = None
    group_name: str | None = None
    result_type: str | None = None
    points: int


class PointsRuleUpdate(BaseModel):
    rule_type: str | None = None
    event_level: str | None = None
    group_name: str | None = None
    result_type: str | None = None
    points: int | None = None
    enabled: bool | None = None


class PointsRuleResponse(BaseModel):
    id: int
    season_id: int
    rule_type: str
    event_level: str | None = None
    group_name: str | None = None
    result_type: str | None = None
    points: int
    enabled: bool
