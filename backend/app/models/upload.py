from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Index, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Upload(Base):
    __tablename__ = "uploads"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tournament_id: Mapped[int] = mapped_column(ForeignKey("tournaments.id"))
    filename: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(20), default="pending")
    total_rows: Mapped[Optional[int]] = mapped_column(Integer, default=None)
    valid_rows: Mapped[Optional[int]] = mapped_column(Integer, default=None)
    error_rows: Mapped[Optional[int]] = mapped_column(Integer, default=None)
    error_log: Mapped[Optional[str]] = mapped_column(Text, default=None)
    preview_data: Mapped[Optional[dict]] = mapped_column(JSON, default=None)
    uploaded_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    __table_args__ = (
        Index("ix_uploads_tournament_id", "tournament_id"),
    )
