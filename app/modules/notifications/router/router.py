from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.modules.notifications.schemas.schemas import NotificationRead
from app.modules.notifications.service.service import NotificationService

router = APIRouter(prefix="/notifications", tags=["notifications"])
service = NotificationService()


@router.get("", response_model=list[NotificationRead])
async def list_notifications(
    session: AsyncSession = Depends(get_db_session),
) -> list[NotificationRead]:
    notifications = await service.list_notifications(session)
    return [NotificationRead.model_validate(notification) for notification in notifications]
