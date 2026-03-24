import pytest

from app.modules.alerts.schemas.schemas import AlertCreate, AlertUpdate
from app.modules.alerts.service.service import AlertService, AlertValidationError
from app.modules.shared.enums import WeatherEventType


@pytest.mark.asyncio
async def test_given_existing_field_when_creating_alert_then_service_returns_persisted_alert(seeded_db_session):
    service = AlertService()

    created_alert = await service.create_alert(
        seeded_db_session,
        AlertCreate(field_id=1, event_type=WeatherEventType.RAIN, threshold=70),
    )

    assert created_alert.id is not None
    assert created_alert.field_id == 1
    assert created_alert.event_type == WeatherEventType.RAIN


@pytest.mark.asyncio
async def test_given_missing_field_when_creating_alert_then_service_raises_validation_error(
    seeded_db_session,
):
    service = AlertService()

    with pytest.raises(AlertValidationError, match="Field 999 does not exist."):
        await service.create_alert(
            seeded_db_session,
            AlertCreate(field_id=999, event_type=WeatherEventType.RAIN, threshold=70),
        )


@pytest.mark.asyncio
async def test_given_empty_update_payload_when_updating_alert_then_service_raises_validation_error(
    seeded_db_session,
):
    service = AlertService()
    created_alert = await service.create_alert(
        seeded_db_session,
        AlertCreate(field_id=1, event_type=WeatherEventType.RAIN, threshold=70),
    )

    with pytest.raises(AlertValidationError, match="At least one field must be provided for update."):
        await service.update_alert(
            seeded_db_session,
            created_alert.id,
            AlertUpdate(),
        )

