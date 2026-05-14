from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AuthenticationError
from app.core.security import create_access_token, hash_password, verify_password
from app.core.config import settings
from app.models.user import User
from sqlalchemy import select


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def login(self, username: str, password: str) -> dict:
        result = await self.db.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()

        if user is None or not verify_password(password, user.password_hash):
            raise AuthenticationError(
                detail="用户名或密码错误", code="AUTH_CREDENTIALS_INVALID"
            )

        if not user.is_active:
            raise AuthenticationError(
                detail="账号已被禁用，请联系管理员", code="AUTH_ACCOUNT_DISABLED"
            )

        token = create_access_token({"sub": str(user.id)})
        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": settings.JWT_EXPIRE_HOURS * 3600,
            "user": {
                "id": user.id,
                "username": user.username,
                "display_name": user.display_name,
            },
        }
