from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.player_repo import PlayerRepository
from app.services.ranking_service import RankingService
from app.services.season_service import SeasonService

router = APIRouter(prefix="/api/v1/public", tags=["public"])


@router.get("/seasons/current", response_model=None)
async def get_current_season(db: AsyncSession = Depends(get_db)):
    service = SeasonService(db)
    season = await service.get_active_season()
    if not season:
        return {"data": None}
    return {
        "data": {
            "id": season.id,
            "name": season.name,
            "start_date": str(season.start_date),
            "end_date": str(season.end_date),
            "status": season.status,
        }
    }


@router.get("/rankings", response_model=None)
async def public_rankings(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = None,
    department: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    service = RankingService(db)
    items, total = await service.get_rankings(page, page_size, search, department)
    return {
        "data": items,
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.get("/players/{player_id}/points", response_model=None)
async def get_player_points(player_id: int, db: AsyncSession = Depends(get_db)):
    service = RankingService(db)
    result = await service.get_player_points(player_id)
    return {"data": result}


@router.get("/departments", response_model=None)
async def get_departments(db: AsyncSession = Depends(get_db)):
    repo = PlayerRepository(db)
    departments = await repo.get_departments()
    return {"data": departments}
