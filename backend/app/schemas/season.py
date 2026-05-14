from datetime import date, datetime

from pydantic import BaseModel


class SeasonCreate(BaseModel):
    name: str
    start_date: date
    end_date: date


class SeasonUpdate(BaseModel):
    name: str | None = None
    start_date: date | None = None
    end_date: date | None = None


class SeasonResponse(BaseModel):
    id: int
    name: str
    start_date: date
    end_date: date
    status: str
    created_at: datetime | None = None
