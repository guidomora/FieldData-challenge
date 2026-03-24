import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.alerts.models.models import Alert
from app.modules.alerts.repository.repository import AlertRepository
from app.modules.alerts.schemas.schemas import AlertCreate, AlertUpdate
from app.modules.fields.repository.repository import FieldRepository

logger = logging.getLogger(__name__)


class AlertValidationError(Exception):
    pass


class AlertService:
    def __init__(
        self,
        repository: AlertRepository | None = None,
        field_repository: FieldRepository | None = None,
    ) -> None:
        self.repository = repository or AlertRepository()
        self.field_repository = field_repository or FieldRepository()

    async def list_alerts(self, session: AsyncSession) -> list[Alert]:
        return await self.repository.list_all(session)

    async def create_alert(self, session: AsyncSession, payload: AlertCreate) -> Alert:
        field = await self.field_repository.get_by_id(session, payload.field_id)
        if field is None:
            logger.warning(
                "Alert creation rejected because field does not exist field_id=%s",
                payload.field_id,
            )
            raise AlertValidationError(f"Field {payload.field_id} does not exist.")

        created_alert = await self.repository.create(session, payload)
        logger.info(
            "Alert created alert_id=%s field_id=%s event_type=%s threshold=%s",
            created_alert.id,
            created_alert.field_id,
            created_alert.event_type,
            created_alert.threshold,
        )
        return created_alert

    async def update_alert(
        self,
        session: AsyncSession,
        alert_id: int,
        payload: AlertUpdate,
    ) -> Alert | None:
        alert = await self.repository.get_by_id(session, alert_id)
        if alert is None:
            logger.warning("Alert update requested for non-existing alert_id=%s", alert_id)
            return None

        if payload.threshold is None and payload.is_active is None:
            logger.warning(
                "Alert update rejected because payload has no mutable fields alert_id=%s",
                alert_id,
            )
            raise AlertValidationError("At least one field must be provided for update.")

        updated_alert = await self.repository.update(session, alert, payload)
        logger.info(
            "Alert updated alert_id=%s threshold=%s is_active=%s",
            updated_alert.id,
            updated_alert.threshold,
            updated_alert.is_active,
        )
        return updated_alert
