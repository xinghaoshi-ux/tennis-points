from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.exceptions import AppException
from app.schemas.player import PlayerCreate, PlayerUpdate
from app.services.player_service import PlayerService

router = APIRouter(prefix="/api/v1/admin/players", tags=["players"])


@router.get("", response_model=None)
async def list_players(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = None,
    department: str | None = None,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = PlayerService(db)
    players, total = await service.list_players(page, page_size, search, department)
    return {
        "data": [
            {
                "id": p.id,
                "full_name": p.full_name,
                "gender": p.gender,
                "birth_date": str(p.birth_date) if p.birth_date else None,
                "department": p.department,
                "status": p.status,
                "created_at": p.created_at.isoformat() if p.created_at else None,
            }
            for p in players
        ],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.post("", response_model=None, status_code=201)
async def create_player(
    body: PlayerCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = PlayerService(db)
    player = await service.create_player(body)
    return {
        "data": {
            "id": player.id,
            "full_name": player.full_name,
            "gender": player.gender,
            "birth_date": str(player.birth_date) if player.birth_date else None,
            "department": player.department,
            "status": player.status,
            "created_at": player.created_at.isoformat() if player.created_at else None,
        },
        "message": "ok",
    }


@router.get("/{player_id}", response_model=None)
async def get_player(
    player_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = PlayerService(db)
    player = await service.get_player(player_id)
    return {
        "data": {
            "id": player.id,
            "full_name": player.full_name,
            "gender": player.gender,
            "birth_date": str(player.birth_date) if player.birth_date else None,
            "department": player.department,
            "status": player.status,
            "created_at": player.created_at.isoformat() if player.created_at else None,
        },
    }


@router.put("/{player_id}", response_model=None)
async def update_player(
    player_id: int,
    body: PlayerUpdate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = PlayerService(db)
    player = await service.update_player(player_id, body)
    return {
        "data": {
            "id": player.id,
            "full_name": player.full_name,
            "gender": player.gender,
            "birth_date": str(player.birth_date) if player.birth_date else None,
            "department": player.department,
            "status": player.status,
            "created_at": player.created_at.isoformat() if player.created_at else None,
        },
        "message": "ok",
    }


@router.delete("/{player_id}", response_model=None)
async def delete_player(
    player_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = PlayerService(db)
    await service.delete_player(player_id)
    return {"message": "ok"}


@router.post("/batch-import", response_model=None, status_code=201)
async def batch_import_players(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    if not file.filename or not file.filename.endswith(".xlsx"):
        raise AppException(detail="仅支持 .xlsx 格式", code="UPLOAD_FILE_TYPE_INVALID", status_code=400)

    service = PlayerService(db)
    result = await service.batch_import(file)
    return {"data": result, "message": "ok"}
