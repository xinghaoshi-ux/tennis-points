from openpyxl import load_workbook
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.player_repo import PlayerRepository
from app.repositories.tournament_repo import TournamentRepository


class ExcelParser:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.player_repo = PlayerRepository(db)
        self.tournament_repo = TournamentRepository(db)

    async def parse(self, file_path: str, tournament_id: int) -> list[dict]:
        tournament = await self.tournament_repo.get_by_id(tournament_id)
        wb = load_workbook(file_path, read_only=True)
        ws = wb.active

        rows = list(ws.iter_rows(min_row=2, values_only=True))
        preview = []

        for idx, row in enumerate(rows, start=1):
            if not row or all(cell is None for cell in row):
                continue

            # Expected columns: result_type, player1_name, player2_name, is_cross_province, is_cross_border
            result_type = str(row[0]).strip() if row[0] else "participant"
            player1_name = str(row[1]).strip() if len(row) > 1 and row[1] else None
            player2_name = str(row[2]).strip() if len(row) > 2 and row[2] else None
            is_cross_province = bool(row[3]) if len(row) > 3 and row[3] else False
            is_cross_border = bool(row[4]) if len(row) > 4 and row[4] else False

            player1_id = None
            player1_matched = False
            player2_id = None
            player2_matched = False
            row_status = "normal"
            error_message = None

            if player1_name:
                p1 = await self.player_repo.get_by_name(player1_name)
                if p1:
                    player1_id = p1.id
                    player1_matched = True
                else:
                    row_status = "warning"
                    error_message = f"选手'{player1_name}'未匹配"

            if player2_name:
                p2 = await self.player_repo.get_by_name(player2_name)
                if p2:
                    player2_id = p2.id
                    player2_matched = True
                else:
                    if error_message:
                        error_message += f"；选手'{player2_name}'未匹配"
                    else:
                        error_message = f"选手'{player2_name}'未匹配"
                    row_status = "warning"

            preview.append({
                "row_number": idx,
                "tournament_name": tournament.name if tournament else None,
                "level": tournament.level if tournament else None,
                "group_name": tournament.group_name if tournament else None,
                "result_type": result_type,
                "player1_name": player1_name,
                "player1_id": player1_id,
                "player1_matched": player1_matched,
                "player2_name": player2_name,
                "player2_id": player2_id,
                "player2_matched": player2_matched,
                "is_cross_province": is_cross_province,
                "is_cross_border": is_cross_border,
                "estimated_points": None,
                "row_status": row_status,
                "error_message": error_message,
            })

        wb.close()
        return preview
