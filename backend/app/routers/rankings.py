from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.services.points_service import PointsService
from app.services.ranking_service import RankingService

router = APIRouter(prefix="/api/v1/admin", tags=["rankings"])


@router.get("/rankings", response_model=None)
async def admin_rankings(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = None,
    department: str | None = None,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = RankingService(db)
    items, total = await service.get_rankings(page, page_size, search, department)
    return {
        "data": items,
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.post("/rankings/refresh", response_model=None, status_code=202)
async def refresh_rankings(
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = RankingService(db)
    result = await service.refresh()
    return {"data": result}


@router.post("/tournaments/{tournament_id}/generate-points", response_model=None, status_code=202)
async def generate_points(
    tournament_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = PointsService(db)
    result = await service.generate_points(tournament_id)
    return {"data": result}
