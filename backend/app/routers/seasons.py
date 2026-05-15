from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.schemas.season import SeasonCreate, SeasonUpdate
from app.services.season_service import SeasonService

router = APIRouter(prefix="/api/v1/admin/seasons", tags=["seasons"])


@router.get("", response_model=None)
async def list_seasons(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = SeasonService(db)
    seasons, total = await service.list_seasons(page, page_size)
    return {
        "data": [
            {
                "id": s.id,
                "name": s.name,
                "start_date": str(s.start_date),
                "end_date": str(s.end_date),
                "status": s.status,
                "created_at": s.created_at.isoformat() if s.created_at else None,
            }
            for s in seasons
        ],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.post("", response_model=None, status_code=201)
async def create_season(
    body: SeasonCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = SeasonService(db)
    season = await service.create_season(body)
    return {
        "data": {
            "id": season.id,
            "name": season.name,
            "start_date": str(season.start_date),
            "end_date": str(season.end_date),
            "status": season.status,
            "created_at": season.created_at.isoformat() if season.created_at else None,
        },
        "message": "ok",
    }


@router.put("/{season_id}", response_model=None)
async def update_season(
    season_id: int,
    body: SeasonUpdate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = SeasonService(db)
    season = await service.update_season(season_id, body)
    return {
        "data": {
            "id": season.id,
            "name": season.name,
            "start_date": str(season.start_date),
            "end_date": str(season.end_date),
            "status": season.status,
            "created_at": season.created_at.isoformat() if season.created_at else None,
        },
        "message": "ok",
    }


@router.post("/{season_id}/activate", response_model=None)
async def activate_season(
    season_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = SeasonService(db)
    season = await service.activate_season(season_id)
    return {
        "data": {
            "id": season.id,
            "name": season.name,
            "start_date": str(season.start_date),
            "end_date": str(season.end_date),
            "status": season.status,
        },
        "message": "ok",
    }


@router.post("/{season_id}/close", response_model=None)
async def close_season(
    season_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = SeasonService(db)
    season = await service.close_season(season_id)
    return {
        "data": {
            "id": season.id,
            "name": season.name,
            "start_date": str(season.start_date),
            "end_date": str(season.end_date),
            "status": season.status,
        },
        "message": "ok",
    }


@router.delete("/{season_id}", response_model=None)
async def delete_season(
    season_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = SeasonService(db)
    await service.delete_season(season_id)
    return {"message": "ok"}
