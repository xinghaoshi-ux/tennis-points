from sqlalchemy import ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class EventResultPlayer(Base):
    __tablename__ = "event_result_players"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    event_result_id: Mapped[int] = mapped_column(ForeignKey("event_results.id"))
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))

    __table_args__ = (
        Index("ix_event_result_players_event_result_id", "event_result_id"),
        Index("ix_event_result_players_player_id", "player_id"),
        UniqueConstraint("event_result_id", "player_id", name="uq_event_result_player"),
    )
