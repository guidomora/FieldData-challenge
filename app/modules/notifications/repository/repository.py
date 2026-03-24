from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.notifications.models.models import Notification
from app.modules.shared.enums import NotificationStatus
from app.modules.weather.models.models import WeatherForecast
from app.modules.alerts.models.models import Alert


class NotificationRepository:
    async def list_all(self, session: AsyncSession) -> list[Notification]:
        result = await session.execute(select(Notification).order_by(Notification.id))
        return list(result.scalars().all())

    async def get_by_alert_and_forecast(
        self,
        session: AsyncSession,
        *,
        alert_id: int,
        forecast_id: int,
    ) -> Notification | None:
        result = await session.execute(
            select(Notification)
            .where(Notification.alert_id == alert_id)
            .where(Notification.forecast_id == forecast_id)
        )
        return result.scalar_one_or_none()

    async def create_for_alert(
        self,
        session: AsyncSession,
        *,
        alert: Alert,
        forecast: WeatherForecast,
    ) -> Notification:
        notification = Notification(
            alert_id=alert.id,
            forecast_id=forecast.id,
            status=NotificationStatus.PENDING,
            message=(
                f"Field {alert.field_id} has a {forecast.event_type} forecast for "
                f"{forecast.forecast_date} with probability {forecast.probability}%."
            ),
        )
        session.add(notification)
        await session.flush()
        return notification
