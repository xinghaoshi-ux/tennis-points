from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.schemas.tournament import TournamentCreate, TournamentUpdate
from app.services.tournament_service import TournamentService

router = APIRouter(prefix="/api/v1/admin/tournaments", tags=["tournaments"])


@router.get("", response_model=None)
async def list_tournaments(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str | None = None,
    season_id: int | None = None,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = TournamentService(db)
    tournaments, total = await service.list_tournaments(page, page_size, status, season_id)
    return {
        "data": [
            {
                "id": t.id,
                "season_id": t.season_id,
                "name": t.name,
                "event_category": t.event_category,
                "level": t.level,
                "group_name": t.group_name,
                "start_date": str(t.start_date) if t.start_date else None,
                "end_date": str(t.end_date) if t.end_date else None,
                "location": t.location,
                "status": t.status,
                "created_at": t.created_at.isoformat() if t.created_at else None,
            }
            for t in tournaments
        ],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.post("", response_model=None, status_code=201)
async def create_tournament(
    body: TournamentCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = TournamentService(db)
    t = await service.create_tournament(body)
    return {
        "data": {
            "id": t.id,
            "season_id": t.season_id,
            "name": t.name,
            "event_category": t.event_category,
            "level": t.level,
            "group_name": t.group_name,
            "start_date": str(t.start_date) if t.start_date else None,
            "end_date": str(t.end_date) if t.end_date else None,
            "location": t.location,
            "status": t.status,
            "created_at": t.created_at.isoformat() if t.created_at else None,
        },
        "message": "ok",
    }


@router.get("/{tournament_id}", response_model=None)
async def get_tournament(
    tournament_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = TournamentService(db)
    t = await service.get_tournament(tournament_id)
    return {
        "data": {
            "id": t.id,
            "season_id": t.season_id,
            "name": t.name,
            "event_category": t.event_category,
            "level": t.level,
            "group_name": t.group_name,
            "start_date": str(t.start_date) if t.start_date else None,
            "end_date": str(t.end_date) if t.end_date else None,
            "location": t.location,
            "status": t.status,
            "created_at": t.created_at.isoformat() if t.created_at else None,
        },
    }


@router.put("/{tournament_id}", response_model=None)
async def update_tournament(
    tournament_id: int,
    body: TournamentUpdate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = TournamentService(db)
    t = await service.update_tournament(tournament_id, body)
    return {
        "data": {
            "id": t.id,
            "season_id": t.season_id,
            "name": t.name,
            "event_category": t.event_category,
            "level": t.level,
            "group_name": t.group_name,
            "start_date": str(t.start_date) if t.start_date else None,
            "end_date": str(t.end_date) if t.end_date else None,
            "location": t.location,
            "status": t.status,
            "created_at": t.created_at.isoformat() if t.created_at else None,
        },
        "message": "ok",
    }


@router.post("/{tournament_id}/revoke-publish", response_model=None)
async def revoke_publish(
    tournament_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = TournamentService(db)
    t = await service.revoke_publish(tournament_id)
    return {
        "data": {
            "id": t.id,
            "name": t.name,
            "status": t.status,
        },
        "message": "ok",
    }


@router.delete("/{tournament_id}", response_model=None)
async def delete_tournament(
    tournament_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = TournamentService(db)
    await service.delete_tournament(tournament_id)
    return {"message": "ok"}
