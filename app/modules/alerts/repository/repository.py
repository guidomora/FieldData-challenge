from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.alerts.models.models import Alert
from app.modules.alerts.schemas.schemas import AlertCreate, AlertUpdate


class AlertRepository:
    async def list_all(self, session: AsyncSession) -> list[Alert]:
        result = await session.execute(select(Alert).order_by(Alert.id))
        return list(result.scalars().all())

    async def list_active(self, session: AsyncSession) -> list[Alert]:
        result = await session.execute(
            select(Alert).where(Alert.is_active.is_(True)).order_by(Alert.id)
        )
        return list(result.scalars().all())

    async def create(self, session: AsyncSession, payload: AlertCreate) -> Alert:
        alert = Alert(**payload.model_dump())
        session.add(alert)
        await session.commit()
        await session.refresh(alert)
        return alert

    async def get_by_id(self, session: AsyncSession, alert_id: int) -> Alert | None:
        result = await session.execute(select(Alert).where(Alert.id == alert_id))
        return result.scalar_one_or_none()

    async def update(
        self,
        session: AsyncSession,
        alert: Alert,
        payload: AlertUpdate,
    ) -> Alert:
        for field_name, value in payload.model_dump(exclude_unset=True).items():
            setattr(alert, field_name, value)

        await session.commit()
        await session.refresh(alert)
        return alert
