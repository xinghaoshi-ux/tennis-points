from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entries_points import EntriesPoints
from app.models.tournament import Tournament
from app.repositories.event_result_repo import EventResultRepository
from app.repositories.points_rule_repo import PointsRuleRepository


class PointsGenerator:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.event_result_repo = EventResultRepository(db)
        self.points_rule_repo = PointsRuleRepository(db)

    async def generate(self, tournament: Tournament):
        event_results = await self.event_result_repo.get_by_tournament(tournament.id)
        rules = await self.points_rule_repo.list(season_id=tournament.season_id)

        for result in event_results:
            points_value = self._match_rule(rules, tournament, result)
            player_ids = await self.event_result_repo.get_players_for_result(result.id)

            if result.team_id and result.team_member_count and result.team_member_count > 0:
                # Team share: split points among members
                share = round(points_value / result.team_member_count)
                for pid in player_ids:
                    self.db.add(EntriesPoints(
                        player_id=pid,
                        tournament_id=tournament.id,
                        season_id=tournament.season_id,
                        source_type="team_share",
                        points_earned=share,
                        result_type=result.result_type,
                        description=f"团队{result.result_type} {points_value} 分，{result.team_member_count} 人分摊",
                        team_id=result.team_id,
                        team_total_points=points_value,
                        team_member_count=result.team_member_count,
                        event_result_id=result.id,
                    ))
            else:
                # Individual: each player gets full points
                for pid in player_ids:
                    self.db.add(EntriesPoints(
                        player_id=pid,
                        tournament_id=tournament.id,
                        season_id=tournament.season_id,
                        source_type="individual_event",
                        points_earned=points_value,
                        result_type=result.result_type,
                        description=f"{tournament.name} {tournament.group_name or ''} {result.result_type}".strip(),
                        event_result_id=result.id,
                    ))

                # Travel bonus
                for pid in player_ids:
                    if result.is_cross_border:
                        self.db.add(EntriesPoints(
                            player_id=pid,
                            tournament_id=tournament.id,
                            season_id=tournament.season_id,
                            source_type="travel_bonus",
                            points_earned=500,
                            description="跨境参赛奖补",
                            event_result_id=result.id,
                        ))
                    elif result.is_cross_province:
                        self.db.add(EntriesPoints(
                            player_id=pid,
                            tournament_id=tournament.id,
                            season_id=tournament.season_id,
                            source_type="travel_bonus",
                            points_earned=200,
                            description="跨省参赛奖补",
                            event_result_id=result.id,
                        ))

        await self.db.flush()

    def _match_rule(self, rules, tournament: Tournament, result) -> int:
        for rule in rules:
            if rule.rule_type != "individual_event" and rule.rule_type != "team_event":
                continue
            if rule.event_level and rule.event_level != tournament.level:
                continue
            if rule.group_name and rule.group_name != "通用" and rule.group_name != tournament.group_name:
                continue
            if rule.result_type and rule.result_type != result.result_type:
                continue
            if rule.enabled:
                return rule.points
        return 0
