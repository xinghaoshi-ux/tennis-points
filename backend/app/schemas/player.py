from datetime import date, datetime

from pydantic import BaseModel


class PlayerCreate(BaseModel):
    full_name: str
    gender: str | None = None
    birth_date: date | None = None
    department: str | None = None
    phone: str | None = None


class PlayerUpdate(BaseModel):
    full_name: str | None = None
    gender: str | None = None
    birth_date: date | None = None
    department: str | None = None
    phone: str | None = None


class PlayerResponse(BaseModel):
    id: int
    full_name: str
    gender: str | None = None
    birth_date: date | None = None
    department: str | None = None
    status: str
    created_at: datetime | None = None
