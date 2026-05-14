import os
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import BusinessConflictError, NotFoundError
from app.models.event_result import EventResult
from app.models.event_result_player import EventResultPlayer
from app.repositories.event_result_repo import EventResultRepository
from app.repositories.player_repo import PlayerRepository
from app.repositories.tournament_repo import TournamentRepository
from app.repositories.upload_repo import UploadRepository


class UploadService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = UploadRepository(db)
        self.tournament_repo = TournamentRepository(db)
        self.player_repo = PlayerRepository(db)
        self.event_result_repo = EventResultRepository(db)

    async def create_upload(self, file: UploadFile, tournament_id: int, user_id: int):
        tournament = await self.tournament_repo.get_by_id(tournament_id)
        if not tournament:
            raise NotFoundError(detail="赛事不存在", code="TOURNAMENT_NOT_FOUND")

        upload_dir = Path(settings.UPLOAD_DIR)
        upload_dir.mkdir(parents=True, exist_ok=True)

        import uuid
        ext = Path(file.filename).suffix
        stored_name = f"{uuid.uuid4().hex}{ext}"
        file_path = upload_dir / stored_name

        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        upload = await self.repo.create(
            tournament_id=tournament_id,
            filename=file.filename,
            file_path=str(file_path),
            uploaded_by=user_id,
        )
        await self.db.commit()

        # In MVP, parse synchronously for simplicity (no ARQ worker required for basic flow)
        await self._parse_excel(upload)
        return upload

    async def get_upload(self, upload_id: int):
        upload = await self.repo.get_by_id(upload_id)
        if not upload:
            raise NotFoundError(detail="上传记录不存在", code="UPLOAD_NOT_FOUND")
        return upload

    async def get_preview(self, upload_id: int):
        upload = await self.repo.get_by_id(upload_id)
        if not upload:
            raise NotFoundError(detail="上传记录不存在", code="UPLOAD_NOT_FOUND")
        if upload.status not in ("parsed", "imported"):
            raise BusinessConflictError(
                detail="上传尚未解析完成", code="UPLOAD_STATUS_INVALID"
            )
        return upload.preview_data or []

    async def confirm_import(self, upload_id: int, confirmed_rows: list[int], ignored_rows: list[int]):
        upload = await self.repo.get_by_id(upload_id)
        if not upload:
            raise NotFoundError(detail="上传记录不存在", code="UPLOAD_NOT_FOUND")
        if upload.status != "parsed":
            raise BusinessConflictError(
                detail="仅 parsed 状态可确认导入", code="UPLOAD_STATUS_INVALID"
            )

        preview = upload.preview_data or []
        imported_count = 0

        for row in preview:
            if row["row_number"] not in confirmed_rows:
                continue
            if row.get("row_status") == "error":
                continue

            event_result = await self.event_result_repo.create(
                tournament_id=upload.tournament_id,
                result_type=row.get("result_type", "participant"),
                is_cross_province=row.get("is_cross_province", False),
                is_cross_border=row.get("is_cross_border", False),
                upload_id=upload.id,
            )

            if row.get("player1_id"):
                await self.event_result_repo.create_player_link(event_result.id, row["player1_id"])
            if row.get("player2_id"):
                await self.event_result_repo.create_player_link(event_result.id, row["player2_id"])

            imported_count += 1

        # Update tournament status to completed
        tournament = await self.tournament_repo.get_by_id(upload.tournament_id)
        if tournament and tournament.status == "draft":
            tournament.status = "completed"

        upload.status = "imported"
        await self.db.commit()

        return {
            "upload_id": upload.id,
            "status": "imported",
            "imported_count": imported_count,
            "ignored_count": len(ignored_rows),
        }

    async def cancel_upload(self, upload_id: int):
        upload = await self.repo.get_by_id(upload_id)
        if not upload:
            raise NotFoundError(detail="上传记录不存在", code="UPLOAD_NOT_FOUND")
        if upload.status not in ("pending", "parsed"):
            raise BusinessConflictError(
                detail="当前状态不可取消", code="UPLOAD_STATUS_INVALID"
            )
        upload.status = "cancelled"
        await self.db.commit()
        return upload

    async def _parse_excel(self, upload):
        from app.processors.excel_parser import ExcelParser

        upload.status = "parsing"
        await self.db.commit()

        try:
            parser = ExcelParser(self.db)
            preview_data = await parser.parse(upload.file_path, upload.tournament_id)
            upload.preview_data = preview_data
            upload.status = "parsed"
            upload.total_rows = len(preview_data)
            upload.valid_rows = sum(1 for r in preview_data if r["row_status"] == "normal")
            upload.error_rows = sum(1 for r in preview_data if r["row_status"] != "normal")
            await self.db.commit()
        except Exception as e:
            upload.status = "parse_failed"
            upload.error_log = str(e)
            await self.db.commit()
