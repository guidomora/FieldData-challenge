from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.fields.models.models import Field


class FieldRepository:
    async def list_all(self, session: AsyncSession) -> list[Field]:
        result = await session.execute(select(Field).order_by(Field.id))
        return list(result.scalars().all())

    async def get_by_id(self, session: AsyncSession, field_id: int) -> Field | None:
        result = await session.execute(select(Field).where(Field.id == field_id))
        return result.scalar_one_or_none()
