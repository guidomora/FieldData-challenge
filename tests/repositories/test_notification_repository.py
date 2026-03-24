from datetime import date

import pytest
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.modules.alerts.models.models import Alert
from app.modules.fields.models.models import Field
from app.modules.notifications.repository.repository import NotificationRepository
from app.modules.shared.enums import NotificationStatus
from app.modules.shared.enums import WeatherEventType
from app.modules.weather.models.models import WeatherForecast


@pytest.mark.asyncio
async def test_given_alert_and_forecast_when_creating_notification_then_repository_builds_pending_notification(
    seeded_db_session,
):
    repository = NotificationRepository()
    result = await seeded_db_session.execute(
        select(Field).options(selectinload(Field.user)).where(Field.id == 1)
    )
    field = result.scalar_one()

    alert = Alert(
        field_id=field.id,
        field=field,
        event_type=WeatherEventType.RAIN,
        threshold=70,
        is_active=True,
    )
    forecast = WeatherForecast(
        field_id=field.id,
        event_type=WeatherEventType.RAIN,
        forecast_date=date.today(),
        probability=80,
        source="test",
    )
    seeded_db_session.add_all([alert, forecast])
    await seeded_db_session.flush()

    created_notification = await repository.create_for_alert(
        seeded_db_session,
        alert=alert,
        forecast=forecast,
    )

    assert created_notification.id is not None
    assert created_notification.alert_id == alert.id
    assert created_notification.forecast_id == forecast.id
    assert created_notification.status == NotificationStatus.PENDING
    assert created_notification.channel == "whatsapp"
    assert created_notification.recipient == "+5491111111111"
    assert "probability 80" in created_notification.message
