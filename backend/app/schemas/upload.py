from datetime import datetime

from pydantic import BaseModel


class UploadResponse(BaseModel):
    id: int
    tournament_id: int
    filename: str
    status: str
    total_rows: int | None = None
    valid_rows: int | None = None
    error_rows: int | None = None
    error_log: str | None = None
    created_at: datetime | None = None


class UploadPreviewRow(BaseModel):
    row_number: int
    tournament_name: str | None = None
    level: str | None = None
    group_name: str | None = None
    result_type: str | None = None
    player1_name: str | None = None
    player1_id: int | None = None
    player1_matched: bool = False
    player2_name: str | None = None
    player2_id: int | None = None
    player2_matched: bool = False
    is_cross_province: bool = False
    is_cross_border: bool = False
    estimated_points: int | None = None
    row_status: str = "normal"
    error_message: str | None = None


class ConfirmImportRequest(BaseModel):
    confirmed_rows: list[int]
    ignored_rows: list[int] = []


class ConfirmImportResponse(BaseModel):
    upload_id: int
    status: str
    imported_count: int
    ignored_count: int
