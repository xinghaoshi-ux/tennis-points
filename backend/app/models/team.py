from datetime import datetime
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    department: Mapped[Optional[str]] = mapped_column(String(100), default=None)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
