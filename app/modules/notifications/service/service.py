from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.notifications.models.models import Notification
from app.modules.notifications.repository.repository import NotificationRepository


class NotificationService:
    def __init__(self, repository: NotificationRepository | None = None) -> None:
        self.repository = repository or NotificationRepository()

    async def list_notifications(self, session: AsyncSession) -> list[Notification]:
        return await self.repository.list_all(session)

