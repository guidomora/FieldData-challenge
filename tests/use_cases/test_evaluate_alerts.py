import pytest

from app.modules.alerts.schemas.schemas import AlertCreate
from app.modules.alerts.service.service import AlertService
from app.modules.alerts.use_cases.evaluate_alerts import AlertEvaluatorUseCase
from app.modules.notifications.repository.repository import NotificationRepository
from app.modules.shared.enums import WeatherEventType


@pytest.mark.asyncio
async def test_given_matching_forecast_when_evaluating_alerts_then_notification_is_created_once(
    seeded_db_session,
):
    alert_service = AlertService()
    use_case = AlertEvaluatorUseCase()
    notification_repository = NotificationRepository()

    await alert_service.create_alert(
        seeded_db_session,
        AlertCreate(field_id=1, event_type=WeatherEventType.RAIN, threshold=70),
    )

    first_result = await use_case.execute(seeded_db_session)
    second_result = await use_case.execute(seeded_db_session)
    notifications = await notification_repository.list_all(seeded_db_session)

    assert first_result.processed_alerts == 1
    assert first_result.notifications_created == 1
    assert second_result.notifications_created == 0
    assert len(notifications) == 1


@pytest.mark.asyncio
async def test_given_non_matching_alert_when_evaluating_alerts_then_no_notification_is_created(
    seeded_db_session,
):
    alert_service = AlertService()
    use_case = AlertEvaluatorUseCase()
    notification_repository = NotificationRepository()

    await alert_service.create_alert(
        seeded_db_session,
        AlertCreate(field_id=1, event_type=WeatherEventType.FROST, threshold=100),
    )

    result = await use_case.execute(seeded_db_session)
    notifications = await notification_repository.list_all(seeded_db_session)

    assert result.processed_alerts == 1
    assert result.notifications_created == 0
    assert notifications == []

