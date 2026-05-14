from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.exceptions import AuthenticationError
from app.core.security import verify_token


async def get_current_user(authorization: str | None = Header(None), db: AsyncSession = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise AuthenticationError(detail="未提供认证 Token", code="AUTH_TOKEN_MISSING")

    token = authorization.removeprefix("Bearer ")
    payload = verify_token(token)
    if payload is None:
        raise AuthenticationError(detail="Token 无效或已过期", code="AUTH_TOKEN_INVALID")

    from app.models.user import User
    from sqlalchemy import select

    user_id = payload.get("sub")
    if user_id is None:
        raise AuthenticationError(detail="Token 无效", code="AUTH_TOKEN_INVALID")

    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()
    if user is None or not user.is_active:
        raise AuthenticationError(detail="用户不存在或已禁用", code="AUTH_ACCOUNT_DISABLED")

    return user
