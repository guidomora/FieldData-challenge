"""seed demo data

Revision ID: 20260323_0002
Revises: 20260323_0001
Create Date: 2026-03-23 18:00:00
"""

from datetime import date, timedelta

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


revision = "20260323_0002"
down_revision = "20260323_0001"
branch_labels = None
depends_on = None


users_table = table(
    "users",
    column("id", sa.Integer),
    column("name", sa.String),
    column("phone_number", sa.String),
)

fields_table = table(
    "fields",
    column("id", sa.Integer),
    column("user_id", sa.Integer),
    column("name", sa.String),
    column("location_name", sa.String),
)

weather_forecasts_table = table(
    "weather_forecasts",
    column("field_id", sa.Integer),
    column("event_type", sa.String),
    column("forecast_date", sa.Date),
    column("probability", sa.Numeric),
    column("source", sa.String),
)


def upgrade() -> None:
    op.bulk_insert(
        users_table,
        [
            {"id": 1, "name": "Juan Perez", "phone_number": "+5491111111111"},
            {"id": 2, "name": "Maria Gomez", "phone_number": "+5491122222222"},
        ],
    )

    op.bulk_insert(
        fields_table,
        [
            {"id": 1, "user_id": 1, "name": "Lote Norte", "location_name": "Pergamino, Buenos Aires"},
            {"id": 2, "user_id": 1, "name": "Lote Sur", "location_name": "Junin, Buenos Aires"},
            {"id": 3, "user_id": 2, "name": "Campo Este", "location_name": "Rio Cuarto, Cordoba"},
        ],
    )
    op.execute("SELECT setval(pg_get_serial_sequence('users', 'id'), 2, true)")
    op.execute("SELECT setval(pg_get_serial_sequence('fields', 'id'), 3, true)")

    today = date.today()
    op.bulk_insert(
        weather_forecasts_table,
        [
            {
                "field_id": 1,
                "event_type": "rain",
                "forecast_date": today + timedelta(days=1),
                "probability": 72,
                "source": "mock_ingestion",
            },
            {
                "field_id": 1,
                "event_type": "frost",
                "forecast_date": today + timedelta(days=2),
                "probability": 41,
                "source": "mock_ingestion",
            },
            {
                "field_id": 2,
                "event_type": "wind",
                "forecast_date": today + timedelta(days=1),
                "probability": 63,
                "source": "mock_ingestion",
            },
            {
                "field_id": 2,
                "event_type": "hail",
                "forecast_date": today + timedelta(days=3),
                "probability": 28,
                "source": "mock_ingestion",
            },
            {
                "field_id": 3,
                "event_type": "rain",
                "forecast_date": today + timedelta(days=1),
                "probability": 84,
                "source": "mock_ingestion",
            },
            {
                "field_id": 3,
                "event_type": "frost",
                "forecast_date": today + timedelta(days=4),
                "probability": 57,
                "source": "mock_ingestion",
            },
        ],
    )


def downgrade() -> None:
    op.execute("DELETE FROM weather_forecasts")
    op.execute("DELETE FROM fields")
    op.execute("DELETE FROM users")
