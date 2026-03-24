from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.weather.models.models import WeatherForecast
from app.modules.weather.schemas.schemas import WeatherForecastCreate


class WeatherForecastRepository:
    async def list_all(self, session: AsyncSession) -> list[WeatherForecast]:
        result = await session.execute(
            select(WeatherForecast).order_by(WeatherForecast.forecast_date, WeatherForecast.id)
        )
        return list(result.scalars().all())

    async def create(
        self,
        session: AsyncSession,
        payload: WeatherForecastCreate,
    ) -> WeatherForecast:
        forecast = WeatherForecast(**payload.model_dump())
        session.add(forecast)
        await session.commit()
        await session.refresh(forecast)
        return forecast

    async def list_matching_alert(
        self,
        session: AsyncSession,
        *,
        field_id: int,
        event_type: str,
        threshold: float,
    ) -> list[WeatherForecast]:
        result = await session.execute(
            select(WeatherForecast)
            .where(WeatherForecast.field_id == field_id)
            .where(WeatherForecast.event_type == event_type)
            .where(WeatherForecast.forecast_date >= date.today())
            .where(WeatherForecast.probability >= threshold)
            .order_by(WeatherForecast.forecast_date, WeatherForecast.id)
        )
        return list(result.scalars().all())
