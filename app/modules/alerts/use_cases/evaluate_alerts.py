import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.alerts.repository.repository import AlertRepository
from app.modules.alerts.schemas.schemas import AlertEvaluationSummary
from app.modules.notifications.repository.repository import NotificationRepository
from app.modules.weather.repository.repository import WeatherForecastRepository

logger = logging.getLogger(__name__)


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
        logger.info("Starting alert evaluation processed_candidate_alerts=%s", len(alerts))

        for alert in alerts:
            matching_forecasts = await self.weather_repository.list_matching_alert(
                session,
                field_id=alert.field_id,
                event_type=alert.event_type,
                threshold=float(alert.threshold),
            )
            if not matching_forecasts:
                logger.info(
                    "No matching forecasts found for alert_id=%s field_id=%s event_type=%s threshold=%s",
                    alert.id,
                    alert.field_id,
                    alert.event_type,
                    alert.threshold,
                )

            for forecast in matching_forecasts:
                existing_notification = await self.notification_repository.get_by_alert_and_forecast(
                    session,
                    alert_id=alert.id,
                    forecast_id=forecast.id,
                )
                if existing_notification is not None:
                    logger.info(
                        "Skipping duplicated notification for alert_id=%s forecast_id=%s",
                        alert.id,
                        forecast.id,
                    )
                    continue

                await self.notification_repository.create_for_alert(
                    session,
                    alert=alert,
                    forecast=forecast,
                )
                notifications_created += 1
                logger.info(
                    "Notification created for alert_id=%s forecast_id=%s recipient=%s",
                    alert.id,
                    forecast.id,
                    alert.field.user.phone_number,
                )

        await session.commit()
        logger.info(
            "Alert evaluation finished processed_alerts=%s notifications_created=%s",
            len(alerts),
            notifications_created,
        )
        return AlertEvaluationSummary(
            processed_alerts=len(alerts),
            notifications_created=notifications_created,
        )
