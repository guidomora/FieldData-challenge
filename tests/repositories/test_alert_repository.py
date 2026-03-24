import pytest

from app.modules.alerts.repository.repository import AlertRepository
from app.modules.alerts.schemas.schemas import AlertCreate, AlertUpdate
from app.modules.shared.enums import WeatherEventType


@pytest.mark.asyncio
async def test_given_seeded_database_when_creating_alert_then_repository_persists_it(seeded_db_session):
    repository = AlertRepository()

    created_alert = await repository.create(
        seeded_db_session,
        AlertCreate(field_id=1, event_type=WeatherEventType.RAIN, threshold=70),
    )

    assert created_alert.id is not None
    assert created_alert.field_id == 1
    assert created_alert.event_type == WeatherEventType.RAIN
    assert float(created_alert.threshold) == 70
    assert created_alert.is_active is True


@pytest.mark.asyncio
async def test_given_active_and_inactive_alerts_when_listing_active_then_only_active_alerts_are_returned(
    seeded_db_session,
):
    repository = AlertRepository()

    active_alert = await repository.create(
        seeded_db_session,
        AlertCreate(field_id=1, event_type=WeatherEventType.RAIN, threshold=70),
    )
    inactive_alert = await repository.create(
        seeded_db_session,
        AlertCreate(field_id=2, event_type=WeatherEventType.WIND, threshold=50),
    )
    await repository.update(
        seeded_db_session,
        inactive_alert,
        AlertUpdate(is_active=False),
    )

    active_alerts = await repository.list_active(seeded_db_session)

    active_alert_ids = {alert.id for alert in active_alerts}
    assert active_alert.id in active_alert_ids
    assert inactive_alert.id not in active_alert_ids

