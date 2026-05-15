"""Full seed script: creates admin user, season, 5 test players, and points rules."""
import asyncio
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import select, text

from app.core.config import settings
from app.core.security import hash_password
from app.models import Base
from app.models.user import User
from app.models.season import Season
from app.models.player import Player
from app.models.points_rule import PointsRule


PLAYERS_DATA = [
    ("张伟-test", "male", "1985-03-15", "计算机科学与技术系"),
    ("李强-test", "male", "1988-07-22", "电子工程系"),
    ("王磊-test", "male", "1990-01-10", "经济管理学院"),
    ("刘洋-test", "female", "1987-11-05", "自动化系"),
    ("陈晨-test", "male", "1992-04-18", "物理系"),
]

POINTS_RULES = [
    # individual_event rules
    ("individual_event", "THA1000", "甲组", "champion", 1000),
    ("individual_event", "THA1000", "甲组", "runner_up", 600),
    ("individual_event", "THA1000", "甲组", "semifinal", 360),
    ("individual_event", "THA1000", "甲组", "quarterfinal", 210),
    ("individual_event", "THA1000", "甲组", "participant", 120),
    ("individual_event", "THA1000", "乙组", "champion", 500),
    ("individual_event", "THA1000", "乙组", "runner_up", 300),
    ("individual_event", "THA1000", "乙组", "semifinal", 180),
    ("individual_event", "THA1000", "乙组", "quarterfinal", 105),
    ("individual_event", "THA1000", "乙组", "participant", 60),
    ("individual_event", "THA800", "通用", "champion", 800),
    ("individual_event", "THA800", "通用", "runner_up", 480),
    ("individual_event", "THA800", "通用", "semifinal", 280),
    ("individual_event", "THA800", "通用", "quarterfinal", 160),
    ("individual_event", "THA800", "通用", "participant", 80),
    ("individual_event", "THA500", "通用", "champion", 500),
    ("individual_event", "THA500", "通用", "runner_up", 300),
    ("individual_event", "THA500", "通用", "semifinal", 180),
    ("individual_event", "THA500", "通用", "quarterfinal", 110),
    ("individual_event", "THA500", "通用", "participant", 45),
    ("individual_event", "THA200", "通用", "champion", 200),
    ("individual_event", "THA200", "通用", "runner_up", 120),
    ("individual_event", "THA200", "通用", "semifinal", 70),
    ("individual_event", "THA200", "通用", "quarterfinal", 45),
    ("individual_event", "THA200", "通用", "participant", 15),
    # team_event rules
    ("team_event", "THA_S", None, "champion", 3000),
    ("team_event", "THA_S", None, "runner_up", 1800),
    ("team_event", "THA_S", None, "semifinal", 1200),
    ("team_event", "THA_S", None, "participant", 600),
    ("team_event", "THA_A", None, "champion", 1800),
    ("team_event", "THA_A", None, "runner_up", 1200),
    ("team_event", "THA_A", None, "semifinal", 800),
    ("team_event", "THA_A", None, "participant", 200),
    ("team_event", "THA_B", None, "champion", 900),
    ("team_event", "THA_B", None, "runner_up", 600),
    ("team_event", "THA_B", None, "semifinal", 400),
    ("team_event", "THA_B", None, "participant", 100),
    # travel_bonus
    ("travel_bonus", None, None, "cross_border", 500),
    ("travel_bonus", None, None, "cross_province", 200),
    # representative_team
    ("representative_team", None, None, "win", 40),
    ("representative_team", None, None, "loss", 20),
    ("representative_team", None, None, "base", 20),
    # organizer_bonus
    ("organizer_bonus", "THA800", None, "organizer", 800),
    ("organizer_bonus", "THA500", None, "organizer", 500),
    ("organizer_bonus", "THA200", None, "organizer", 200),
    ("organizer_bonus", "THA_A", None, "organizer", 800),
    ("organizer_bonus", "THA_B", None, "organizer", 500),
]

async def seed():
    engine = create_async_engine(settings.async_database_url, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_factory() as db:
        # Clear existing data for a clean slate
        await db.execute(text("DELETE FROM entries_points"))
        await db.execute(text("DELETE FROM event_result_players"))
        await db.execute(text("DELETE FROM event_results"))
        await db.execute(text("DELETE FROM team_members"))
        await db.execute(text("DELETE FROM teams"))
        await db.execute(text("DELETE FROM uploads"))
        await db.execute(text("DELETE FROM tournaments"))
        await db.execute(text("DELETE FROM players"))
        await db.execute(text("DELETE FROM points_rules"))
        await db.execute(text("DELETE FROM seasons"))
        await db.flush()
        print("Cleared existing data")

        # 1. Admin user
        result = await db.execute(select(User).where(User.username == "admin"))
        if not result.scalar_one_or_none():
            db.add(User(username="admin", password_hash=hash_password("admin123"), display_name="管理员"))
            print("Created admin user: admin / admin123")

        # 2. Season
        season = Season(name="2026-2027 THA 赛季", start_date=date(2026, 4, 20), end_date=date(2027, 4, 20), status="active")
        db.add(season)
        await db.flush()
        season_id = season.id
        print(f"Created season (id={season_id})")

        # 3. Players (5 test players)
        players = []
        for name, gender, bd, dept in PLAYERS_DATA:
            p = Player(full_name=name, gender=gender, birth_date=date.fromisoformat(bd), department=dept)
            db.add(p)
            players.append(p)
        await db.flush()
        print(f"Created {len(players)} test players")

        # 4. Points Rules
        for rule_type, level, group, result_type, points in POINTS_RULES:
            db.add(PointsRule(
                season_id=season_id, rule_type=rule_type, event_level=level,
                group_name=group, result_type=result_type, points=points,
            ))
        await db.flush()
        print(f"Created {len(POINTS_RULES)} points rules")

        await db.commit()
    print("Seed complete!")


if __name__ == "__main__":
    asyncio.run(seed())
