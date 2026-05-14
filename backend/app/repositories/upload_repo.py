from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.upload import Upload


class UploadRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, upload_id: int) -> Upload | None:
        result = await self.db.execute(select(Upload).where(Upload.id == upload_id))
        return result.scalar_one_or_none()

    async def create(self, **kwargs) -> Upload:
        upload = Upload(**kwargs)
        self.db.add(upload)
        await self.db.flush()
        return upload

    async def update(self, upload: Upload, **kwargs) -> Upload:
        for key, value in kwargs.items():
            setattr(upload, key, value)
        await self.db.flush()
        return upload
