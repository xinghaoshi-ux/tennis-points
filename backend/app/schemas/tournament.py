from datetime import date, datetime

from pydantic import BaseModel


class TournamentCreate(BaseModel):
    name: str
    event_category: str
    level: str
    group_name: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    location: str | None = None
    alumni_player_count: int | None = None


class TournamentUpdate(BaseModel):
    name: str | None = None
    event_category: str | None = None
    level: str | None = None
    group_name: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    location: str | None = None
    alumni_player_count: int | None = None


class TournamentResponse(BaseModel):
    id: int
    season_id: int
    name: str
    event_category: str
    level: str
    group_name: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    location: str | None = None
    status: str
    created_at: datetime | None = None
