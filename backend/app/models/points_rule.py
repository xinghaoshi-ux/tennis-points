from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class PointsRule(Base):
    __tablename__ = "points_rules"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    season_id: Mapped[int] = mapped_column(ForeignKey("seasons.id"))
    rule_type: Mapped[str] = mapped_column(String(30))
    event_level: Mapped[Optional[str]] = mapped_column(String(20), default=None)
    group_name: Mapped[Optional[str]] = mapped_column(String(50), default=None)
    result_type: Mapped[Optional[str]] = mapped_column(String(30), default=None)
    points: Mapped[int] = mapped_column(Integer)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint(
            "season_id", "rule_type", "event_level", "group_name", "result_type",
            name="uq_points_rule_combo",
        ),
    )
