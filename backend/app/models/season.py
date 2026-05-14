from datetime import date, datetime
from typing import Optional

from sqlalchemy import Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Season(TimestampMixin, Base):
    __tablename__ = "seasons"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    start_date: Mapped[date]
    end_date: Mapped[date]
    status: Mapped[str] = mapped_column(String(20), default="draft")
