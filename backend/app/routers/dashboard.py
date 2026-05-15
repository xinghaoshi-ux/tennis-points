from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.entries_points import EntriesPoints
from app.models.player import Player
from app.models.season import Season
from app.models.tournament import Tournament
from app.models.upload import Upload

router = APIRouter(prefix="/api/v1/admin/dashboard", tags=["dashboard"])


@router.get("", response_model=None)
async def get_dashboard(
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    # Current season
    season_result = await db.execute(select(Season).where(Season.status == "active"))
    active_season = season_result.scalar_one_or_none()

    # Counts
    player_count = (await db.execute(select(func.count(Player.id)))).scalar_one()
    tournament_count = (await db.execute(select(func.count(Tournament.id)))).scalar_one()
    points_count = (await db.execute(select(func.count(EntriesPoints.id)))).scalar_one()

    # Recent uploads
    uploads_result = await db.execute(
        select(Upload).order_by(Upload.created_at.desc()).limit(5)
    )
    recent_uploads = [
        {
            "id": u.id,
            "filename": u.filename,
            "status": u.status,
            "created_at": u.created_at.isoformat() if u.created_at else None,
        }
        for u in uploads_result.scalars().all()
    ]

    return {
        "data": {
            "current_season": {"id": active_season.id, "name": active_season.name} if active_season else None,
            "player_count": player_count,
            "tournament_count": tournament_count,
            "points_record_count": points_count,
            "recent_uploads": recent_uploads,
        }
    }
