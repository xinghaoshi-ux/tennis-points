"""Full seed script: creates admin user, season, players, tournaments, points rules, and ranking data."""
import asyncio
from datetime import date, datetime

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import select, text

from app.core.config import settings
from app.core.security import hash_password
from app.models import Base
from app.models.user import User
from app.models.season import Season
from app.models.player import Player
from app.models.tournament import Tournament
from app.models.points_rule import PointsRule
from app.models.entries_points import EntriesPoints
from app.models.event_result import EventResult
from app.models.event_result_player import EventResultPlayer
from app.models.team import Team


PLAYERS_DATA = [
    ("张伟", "male", "1985-03-15", "计算机科学与技术系"),
    ("李强", "male", "1988-07-22", "电子工程系"),
    ("王磊", "male", "1990-01-10", "经济管理学院"),
    ("刘洋", "male", "1987-11-05", "自动化系"),
    ("陈晨", "male", "1992-04-18", "物理系"),
    ("赵鹏", "male", "1986-09-30", "数学科学系"),
    ("孙浩", "male", "1991-06-12", "机械工程系"),
    ("周明", "male", "1989-02-28", "土木工程系"),
    ("吴刚", "male", "1984-12-01", "化学工程系"),
    ("郑涛", "male", "1993-08-25", "生命科学学院"),
    ("马超", "male", "1988-05-14", "材料科学与工程系"),
    ("黄海", "male", "1990-10-07", "环境学院"),
    ("林峰", "male", "1986-03-20", "建筑学院"),
    ("何军", "male", "1991-12-15", "法学院"),
    ("高远", "male", "1987-07-08", "新闻与传播学院"),
    ("罗杰", "male", "1989-09-03", "计算机科学与技术系"),
    ("谢飞", "male", "1992-01-25", "电子工程系"),
    ("韩冰", "male", "1985-11-18", "经济管理学院"),
    ("唐亮", "male", "1990-04-30", "自动化系"),
    ("冯凯", "male", "1988-08-12", "物理系"),
    ("曹宇", "male", "1993-02-14", "数学科学系"),
    ("彭勇", "male", "1986-06-22", "机械工程系"),
    ("董磊", "male", "1991-10-05", "土木工程系"),
    ("袁志", "male", "1987-03-17", "化学工程系"),
    ("蒋华", "male", "1989-12-28", "生命科学学院"),
    ("王芳", "female", "1990-05-20", "经济管理学院"),
    ("李娜", "female", "1992-08-15", "法学院"),
    ("张敏", "female", "1988-11-03", "新闻与传播学院"),
    ("刘婷", "female", "1991-02-10", "计算机科学与技术系"),
    ("陈静", "female", "1989-07-25", "电子工程系"),
    ("杨洁", "female", "1993-04-08", "环境学院"),
    ("赵丽", "female", "1987-09-12", "建筑学院"),
    ("周颖", "female", "1990-12-30", "材料科学与工程系"),
    ("吴婷", "female", "1988-06-18", "自动化系"),
    ("孙悦", "female", "1991-01-22", "物理系"),
]

TOURNAMENTS_DATA = [
    # (name, event_category, level, group_name, start_date, end_date, location, alumni_count, status)
    ("THA500 成都站", "individual_doubles", "THA500", "甲组", "2026-05-10", "2026-05-12", "成都市网球中心", 38, "published"),
    ("THA500 上海站", "individual_doubles", "THA500", "甲组", "2026-06-15", "2026-06-17", "上海旗忠网球中心", 42, "published"),
    ("THA800 北京站", "individual_doubles", "THA800", "甲组", "2026-07-20", "2026-07-22", "国家网球中心", 55, "published"),
    ("THA200 杭州站", "individual_doubles", "THA200", "甲组", "2026-08-10", "2026-08-11", "杭州黄龙体育中心", 22, "published"),
    ("THA500 深圳站", "individual_doubles", "THA500", "甲组", "2026-09-05", "2026-09-07", "深圳网球中心", 35, "published"),
    ("THA500 成都站（乙组）", "individual_doubles", "THA500", "乙组", "2026-05-10", "2026-05-12", "成都市网球中心", 30, "published"),
    ("THA800 北京站（女双）", "individual_doubles", "THA800", "女双组", "2026-07-20", "2026-07-22", "国家网球中心", 28, "published"),
    ("THA A 级团体赛北京站", "team", "THA_A", None, "2026-10-15", "2026-10-17", "北京奥体中心", 48, "published"),
    ("THA B 级团体赛上海站", "team", "THA_B", None, "2026-11-01", "2026-11-02", "上海源深体育中心", 32, "published"),
    ("开源杯代表队赛", "representative", "representative", None, "2026-09-20", "2026-09-22", "武汉光谷网球中心", 16, "published"),
    ("THA200 广州站", "individual_doubles", "THA200", "甲组", "2026-11-15", "2026-11-16", "广州天河体育中心", 20, "completed"),
    ("THA500 南京站", "individual_doubles", "THA500", "甲组", "2026-12-01", "2026-12-03", "南京奥体中心", 36, "draft"),
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
        # 1. Admin user
        result = await db.execute(select(User).where(User.username == "admin"))
        if not result.scalar_one_or_none():
            db.add(User(username="admin", password_hash=hash_password("admin123"), display_name="管理员"))
            print("Created admin user: admin / admin123")

        # 2. Season
        result = await db.execute(select(Season))
        existing_seasons = result.scalars().all()
        if not existing_seasons:
            season = Season(name="2026-2027 THA 赛季", start_date=date(2026, 4, 20), end_date=date(2027, 4, 20), status="active")
            db.add(season)
            old_season = Season(name="2025-2026 THA 赛季", start_date=date(2025, 4, 20), end_date=date(2026, 4, 19), status="closed")
            db.add(old_season)
            await db.flush()
            season_id = season.id
            print(f"Created seasons (active id={season_id})")
        else:
            season_id = next((s.id for s in existing_seasons if s.status == "active"), existing_seasons[0].id)
            print(f"Seasons exist, using id={season_id}")

        # 3. Players
        result = await db.execute(select(Player))
        if not result.scalars().first():
            players = []
            for name, gender, bd, dept in PLAYERS_DATA:
                p = Player(full_name=name, gender=gender, birth_date=date.fromisoformat(bd), department=dept)
                db.add(p)
                players.append(p)
            await db.flush()
            print(f"Created {len(players)} players")
        else:
            result = await db.execute(select(Player).order_by(Player.id))
            players = list(result.scalars().all())
            print(f"Players exist ({len(players)})")

        # 4. Tournaments
        result = await db.execute(select(Tournament))
        if not result.scalars().first():
            tournaments = []
            for name, cat, level, group, sd, ed, loc, count, status in TOURNAMENTS_DATA:
                t = Tournament(
                    season_id=season_id, name=name, event_category=cat, level=level,
                    group_name=group, start_date=date.fromisoformat(sd),
                    end_date=date.fromisoformat(ed), location=loc,
                    alumni_player_count=count, status=status,
                )
                db.add(t)
                tournaments.append(t)
            await db.flush()
            print(f"Created {len(tournaments)} tournaments")
        else:
            result = await db.execute(select(Tournament).order_by(Tournament.id))
            tournaments = list(result.scalars().all())
            print(f"Tournaments exist ({len(tournaments)})")

        # 5. Points Rules
        result = await db.execute(select(PointsRule))
        if not result.scalars().first():
            for rule_type, level, group, result_type, points in POINTS_RULES:
                db.add(PointsRule(
                    season_id=season_id, rule_type=rule_type, event_level=level,
                    group_name=group, result_type=result_type, points=points,
                ))
            await db.flush()
            print(f"Created {len(POINTS_RULES)} points rules")

        # 6. Generate entries_points for published tournaments
        result = await db.execute(select(EntriesPoints))
        if not result.scalars().first():
            await generate_points_data(db, season_id, players, tournaments)

        await db.commit()
    print("Seed complete!")


async def generate_points_data(db: AsyncSession, season_id: int, players: list, tournaments: list):
    """Generate realistic points data for published tournaments."""
    import random
    random.seed(42)

    published = [t for t in tournaments if t.status == "published"]
    count = 0

    for t in published:
        if t.event_category == "individual_doubles":
            pts_map = get_individual_points(t.level, t.group_name)
            # Pick participants for this tournament
            if t.group_name == "女双组":
                pool = [p for p in players if p.gender == "female"]
            elif t.group_name == "乙组":
                pool = random.sample([p for p in players if p.gender == "male"], min(16, len([p for p in players if p.gender == "male"])))
            else:
                pool = random.sample(players[:25], min(16, 25))

            random.shuffle(pool)
            results = [
                ("champion", pool[0:2]),
                ("runner_up", pool[2:4]),
                ("semifinal", pool[4:6]),
                ("semifinal", pool[6:8]),
                ("quarterfinal", pool[8:10]),
                ("quarterfinal", pool[10:12]),
            ]
            participants = pool[12:]

            for result_type, pair in results:
                pts = pts_map.get(result_type, 0)
                for p in pair:
                    db.add(EntriesPoints(
                        player_id=p.id, tournament_id=t.id, season_id=season_id,
                        source_type="individual_event", points_earned=pts,
                        result_type=result_type, description=f"{t.name} {result_type}",
                    ))
                    count += 1

            for p in participants:
                db.add(EntriesPoints(
                    player_id=p.id, tournament_id=t.id, season_id=season_id,
                    source_type="individual_event", points_earned=pts_map.get("participant", 0),
                    result_type="participant", description=f"{t.name} 参赛",
                ))
                count += 1

            # Travel bonus for some players
            if "成都" in t.name or "深圳" in t.name:
                bonus_players = random.sample(pool[:8], min(3, len(pool[:8])))
                for p in bonus_players:
                    db.add(EntriesPoints(
                        player_id=p.id, tournament_id=t.id, season_id=season_id,
                        source_type="travel_bonus", points_earned=200,
                        result_type="cross_province", description=f"{t.name} 跨省参赛奖补",
                    ))
                    count += 1

        elif t.event_category == "team":
            team_pts_map = get_team_points(t.level)
            male_players = [p for p in players if p.gender == "male"]
            random.shuffle(male_players)

            teams_config = [
                ("计算机学院队", "计算机科学与技术系", "champion", male_players[0:8]),
                ("经管学院队", "经济管理学院", "runner_up", male_players[8:16]),
                ("电子工程队", "电子工程系", "semifinal", male_players[16:22]),
            ]

            for team_name, dept, result_type, members in teams_config:
                team_total = team_pts_map.get(result_type, 0)
                member_count = len(members)
                per_person = round(team_total / member_count) if member_count > 0 else 0
                for p in members:
                    db.add(EntriesPoints(
                        player_id=p.id, tournament_id=t.id, season_id=season_id,
                        source_type="team_share", points_earned=per_person,
                        result_type=result_type,
                        description=f"{t.name} {team_name} {result_type}",
                        team_total_points=team_total, team_member_count=member_count,
                    ))
                    count += 1

        elif t.event_category == "representative":
            # Representative team event
            rep_players = random.sample(players[:20], 8)
            for p in rep_players:
                wins = random.randint(1, 3)
                losses = random.randint(0, 2)
                pts = wins * 40 + losses * 20 + 20
                db.add(EntriesPoints(
                    player_id=p.id, tournament_id=t.id, season_id=season_id,
                    source_type="representative_team", points_earned=pts,
                    result_type=None,
                    description=f"{t.name} {wins}胜{losses}负 + 基础参赛",
                ))
                count += 1

    # Organizer bonus
    organizer_players = random.sample(players[:10], 3)
    org_tournaments = [t for t in published if t.event_category == "individual_doubles"][:3]
    for i, p in enumerate(organizer_players):
        if i < len(org_tournaments):
            ot = org_tournaments[i]
            pts = 500 if "500" in ot.level else (800 if "800" in ot.level else 200)
            db.add(EntriesPoints(
                player_id=p.id, tournament_id=ot.id, season_id=season_id,
                source_type="organizer_bonus", points_earned=pts,
                result_type="organizer", description=f"承办 {ot.name}",
            ))
            count += 1

    await db.flush()
    print(f"Generated {count} entries_points records")


def get_individual_points(level: str, group_name: str | None) -> dict:
    if level == "THA1000":
        if group_name == "乙组":
            return {"champion": 500, "runner_up": 300, "semifinal": 180, "quarterfinal": 105, "participant": 60}
        return {"champion": 1000, "runner_up": 600, "semifinal": 360, "quarterfinal": 210, "participant": 120}
    elif level == "THA800":
        return {"champion": 800, "runner_up": 480, "semifinal": 280, "quarterfinal": 160, "participant": 80}
    elif level == "THA500":
        if group_name == "乙组":
            return {"champion": 250, "runner_up": 150, "semifinal": 90, "quarterfinal": 55, "participant": 22}
        return {"champion": 500, "runner_up": 300, "semifinal": 180, "quarterfinal": 110, "participant": 45}
    elif level == "THA200":
        return {"champion": 200, "runner_up": 120, "semifinal": 70, "quarterfinal": 45, "participant": 15}
    return {"champion": 0, "runner_up": 0, "semifinal": 0, "quarterfinal": 0, "participant": 0}


def get_team_points(level: str) -> dict:
    if level == "THA_S":
        return {"champion": 3000, "runner_up": 1800, "semifinal": 1200, "participant": 600}
    elif level == "THA_A":
        return {"champion": 1800, "runner_up": 1200, "semifinal": 800, "participant": 200}
    elif level == "THA_B":
        return {"champion": 900, "runner_up": 600, "semifinal": 400, "participant": 100}
    return {}


if __name__ == "__main__":
    asyncio.run(seed())
