from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.models.models import User


class UserRepository:
    async def list_all(self, session: AsyncSession) -> list[User]:
        result = await session.execute(select(User).order_by(User.id))
        return list(result.scalars().all())

