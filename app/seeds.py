from datetime import date, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.fields.models.models import Field
from app.modules.shared.enums import WeatherEventType
from app.modules.users.models.models import User
from app.modules.weather.models.models import WeatherForecast


async def seed_demo_data(session: AsyncSession) -> None:
    existing_user_count = await session.scalar(select(func.count()).select_from(User))
    if existing_user_count and existing_user_count > 0:
        return

    users = [
        User(name="Juan Perez", phone_number="+5491111111111"),
        User(name="Maria Gomez", phone_number="+5491122222222"),
    ]
    session.add_all(users)
    await session.flush()

    fields = [
        Field(user_id=users[0].id, name="Lote Norte", location_name="Pergamino, Buenos Aires"),
        Field(user_id=users[0].id, name="Lote Sur", location_name="Junin, Buenos Aires"),
        Field(user_id=users[1].id, name="Campo Este", location_name="Rio Cuarto, Cordoba"),
    ]
    session.add_all(fields)
    await session.flush()

    today = date.today()
    forecasts = [
        WeatherForecast(
            field_id=fields[0].id,
            event_type=WeatherEventType.RAIN,
            forecast_date=today + timedelta(days=1),
            probability=72,
            source="mock_ingestion",
        ),
        WeatherForecast(
            field_id=fields[0].id,
            event_type=WeatherEventType.FROST,
            forecast_date=today + timedelta(days=2),
            probability=41,
            source="mock_ingestion",
        ),
        WeatherForecast(
            field_id=fields[1].id,
            event_type=WeatherEventType.WIND,
            forecast_date=today + timedelta(days=1),
            probability=63,
            source="mock_ingestion",
        ),
        WeatherForecast(
            field_id=fields[1].id,
            event_type=WeatherEventType.HAIL,
            forecast_date=today + timedelta(days=3),
            probability=28,
            source="mock_ingestion",
        ),
        WeatherForecast(
            field_id=fields[2].id,
            event_type=WeatherEventType.RAIN,
            forecast_date=today + timedelta(days=1),
            probability=84,
            source="mock_ingestion",
        ),
        WeatherForecast(
            field_id=fields[2].id,
            event_type=WeatherEventType.FROST,
            forecast_date=today + timedelta(days=4),
            probability=57,
            source="mock_ingestion",
        ),
    ]
    session.add_all(forecasts)
    await session.commit()
