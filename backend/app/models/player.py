from datetime import date, datetime
from typing import Optional

from sqlalchemy import Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Player(TimestampMixin, Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(50))
    gender: Mapped[Optional[str]] = mapped_column(String(10), default=None)
    birth_date: Mapped[Optional[date]] = mapped_column(default=None)
    department: Mapped[Optional[str]] = mapped_column(String(100), default=None)
    phone: Mapped[Optional[str]] = mapped_column(String(20), default=None)
    status: Mapped[str] = mapped_column(String(20), default="active")

    __table_args__ = (
        Index("ix_players_full_name", "full_name"),
        Index("ix_players_department", "department"),
    )
