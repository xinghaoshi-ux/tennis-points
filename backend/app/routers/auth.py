from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.schemas.auth import LoginRequest, LoginResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/v1/admin/auth", tags=["auth"])


@router.post("/login", response_model=None)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    result = await service.login(body.username, body.password)
    return {"data": result}


@router.get("/me", response_model=None)
async def get_me(current_user=Depends(get_current_user)):
    return {
        "data": {
            "id": current_user.id,
            "username": current_user.username,
            "display_name": current_user.display_name,
        }
    }
