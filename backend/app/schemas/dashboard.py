from datetime import datetime

from pydantic import BaseModel


class RecentUpload(BaseModel):
    id: int
    filename: str
    status: str
    created_at: datetime | None = None


class DashboardResponse(BaseModel):
    current_season: str | None = None
    player_count: int
    tournament_count: int
    points_record_count: int
    recent_uploads: list[RecentUpload]
