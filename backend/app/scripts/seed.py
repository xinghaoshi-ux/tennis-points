"""Seed script: creates initial admin user and a draft season."""
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import async_session_factory, engine
from app.core.security import hash_password
from app.models import Base
from app.models.user import User
from app.models.season import Season
from sqlalchemy import select


async def seed():
    async with async_session_factory() as db:
        # Create admin user if not exists
        result = await db.execute(select(User).where(User.username == "admin"))
        if not result.scalar_one_or_none():
            admin = User(
                username="admin",
                password_hash=hash_password("admin123"),
                display_name="管理员",
            )
            db.add(admin)
            print("Created admin user: admin / admin123")
        else:
            print("Admin user already exists")

        # Create initial season if none exists
        result = await db.execute(select(Season))
        if not result.scalars().first():
            from datetime import date
            season = Season(
                name="2026-2027 THA 赛季",
                start_date=date(2026, 4, 20),
                end_date=date(2027, 4, 20),
                status="active",
            )
            db.add(season)
            print("Created initial season: 2026-2027 THA 赛季 (active)")
        else:
            print("Season already exists")

        await db.commit()


if __name__ == "__main__":
    asyncio.run(seed())
