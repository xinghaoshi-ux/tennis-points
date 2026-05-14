from pydantic import BaseModel


class RankingItem(BaseModel):
    ranking: int
    player_id: int
    full_name: str
    department: str | None = None
    age: int | None = None
    total_points: int
    tournament_count: int


class PointsDetailItem(BaseModel):
    id: int
    tournament_name: str
    source_type: str
    result_type: str | None = None
    points_earned: int
    description: str | None = None
    tournament_date: str | None = None
    team_name: str | None = None
    team_total_points: int | None = None
    team_member_count: int | None = None


class PointsSummary(BaseModel):
    individual_event: int = 0
    team_share: int = 0
    travel_bonus: int = 0
    representative_team: int = 0
    organizer_bonus: int = 0
    donation_bonus: int = 0


class PlayerPointsResponse(BaseModel):
    player: RankingItem
    summary: PointsSummary
    details: list[PointsDetailItem]
