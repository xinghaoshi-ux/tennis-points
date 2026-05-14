from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 20


class MessageResponse(BaseModel):
    message: str = "ok"
