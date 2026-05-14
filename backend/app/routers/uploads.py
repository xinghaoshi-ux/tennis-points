from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.exceptions import AppException
from app.schemas.upload import ConfirmImportRequest
from app.services.upload_service import UploadService

router = APIRouter(prefix="/api/v1/admin/uploads", tags=["uploads"])


@router.post("", response_model=None, status_code=201)
async def create_upload(
    file: UploadFile = File(...),
    tournament_id: int = Form(...),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if not file.filename or not file.filename.endswith(".xlsx"):
        raise AppException(detail="仅支持 .xlsx 格式", code="UPLOAD_FILE_TYPE_INVALID", status_code=400)

    service = UploadService(db)
    upload = await service.create_upload(file, tournament_id, current_user.id)
    return {
        "data": {
            "id": upload.id,
            "tournament_id": upload.tournament_id,
            "filename": upload.filename,
            "status": upload.status,
            "created_at": upload.created_at.isoformat() if upload.created_at else None,
        },
    }


@router.get("/{upload_id}", response_model=None)
async def get_upload(
    upload_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = UploadService(db)
    upload = await service.get_upload(upload_id)
    return {
        "data": {
            "id": upload.id,
            "tournament_id": upload.tournament_id,
            "filename": upload.filename,
            "status": upload.status,
            "total_rows": upload.total_rows,
            "valid_rows": upload.valid_rows,
            "error_rows": upload.error_rows,
            "error_log": upload.error_log,
            "created_at": upload.created_at.isoformat() if upload.created_at else None,
        },
    }


@router.get("/{upload_id}/preview", response_model=None)
async def get_preview(
    upload_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = UploadService(db)
    preview = await service.get_preview(upload_id)
    return {"data": preview}


@router.post("/{upload_id}/confirm", response_model=None)
async def confirm_import(
    upload_id: int,
    body: ConfirmImportRequest,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = UploadService(db)
    result = await service.confirm_import(upload_id, body.confirmed_rows, body.ignored_rows)
    return {"data": result}


@router.post("/{upload_id}/cancel", response_model=None)
async def cancel_upload(
    upload_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = UploadService(db)
    upload = await service.cancel_upload(upload_id)
    return {
        "data": {
            "id": upload.id,
            "status": upload.status,
        },
        "message": "ok",
    }
