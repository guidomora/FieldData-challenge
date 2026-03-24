from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.alerts.models.models import Alert
from app.modules.alerts.repository.repository import AlertRepository
from app.modules.alerts.schemas.schemas import AlertCreate, AlertUpdate
from app.modules.fields.repository.repository import FieldRepository


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
            raise AlertValidationError(f"Field {payload.field_id} does not exist.")

        return await self.repository.create(session, payload)

    async def update_alert(
        self,
        session: AsyncSession,
        alert_id: int,
        payload: AlertUpdate,
    ) -> Alert | None:
        alert = await self.repository.get_by_id(session, alert_id)
        if alert is None:
            return None

        if payload.threshold is None and payload.is_active is None:
            raise AlertValidationError("At least one field must be provided for update.")

        return await self.repository.update(session, alert, payload)
