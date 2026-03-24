from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.alerts.repository.repository import AlertRepository
from app.modules.alerts.schemas.schemas import AlertEvaluationSummary
from app.modules.notifications.repository.repository import NotificationRepository
from app.modules.weather.repository.repository import WeatherForecastRepository


class AlertEvaluatorUseCase:
    def __init__(
        self,
        alert_repository: AlertRepository | None = None,
        weather_repository: WeatherForecastRepository | None = None,
        notification_repository: NotificationRepository | None = None,
    ) -> None:
        self.alert_repository = alert_repository or AlertRepository()
        self.weather_repository = weather_repository or WeatherForecastRepository()
        self.notification_repository = notification_repository or NotificationRepository()

    async def execute(self, session: AsyncSession) -> AlertEvaluationSummary:
        alerts = await self.alert_repository.list_active(session)
        notifications_created = 0

        for alert in alerts:
            matching_forecasts = await self.weather_repository.list_matching_alert(
                session,
                field_id=alert.field_id,
                event_type=alert.event_type,
                threshold=float(alert.threshold),
            )

            for forecast in matching_forecasts:
                existing_notification = await self.notification_repository.get_by_alert_and_forecast(
                    session,
                    alert_id=alert.id,
                    forecast_id=forecast.id,
                )
                if existing_notification is not None:
                    continue

                await self.notification_repository.create_for_alert(
                    session,
                    alert=alert,
                    forecast=forecast,
                )
                notifications_created += 1

        await session.commit()
        return AlertEvaluationSummary(
            processed_alerts=len(alerts),
            notifications_created=notifications_created,
        )
