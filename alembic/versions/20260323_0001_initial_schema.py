"""initial schema

Revision ID: 20260323_0001
Revises:
Create Date: 2026-03-23 17:00:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260323_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("phone_number", sa.String(length=30), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("phone_number", name=op.f("uq_users_phone_number")),
    )

    op.create_table(
        "fields",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("location_name", sa.String(length=120), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("fk_fields_user_id_users")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_fields")),
    )
    op.create_index(op.f("ix_fields_user_id"), "fields", ["user_id"], unique=False)

    op.create_table(
        "alerts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("field_id", sa.Integer(), nullable=False),
        sa.Column("event_type", sa.String(length=30), nullable=False),
        sa.Column("threshold", sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("threshold >= 0 AND threshold <= 100", name=op.f("ck_alerts_threshold_range")),
        sa.ForeignKeyConstraint(["field_id"], ["fields.id"], name=op.f("fk_alerts_field_id_fields")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_alerts")),
    )
    op.create_index(op.f("ix_alerts_field_id"), "alerts", ["field_id"], unique=False)
    op.create_index("ix_alerts_field_event_active", "alerts", ["field_id", "event_type", "is_active"], unique=False)

    op.create_table(
        "weather_forecasts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("field_id", sa.Integer(), nullable=False),
        sa.Column("event_type", sa.String(length=30), nullable=False),
        sa.Column("forecast_date", sa.Date(), nullable=False),
        sa.Column("probability", sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column("source", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("probability >= 0 AND probability <= 100", name=op.f("ck_weather_forecasts_probability_range")),
        sa.ForeignKeyConstraint(["field_id"], ["fields.id"], name=op.f("fk_weather_forecasts_field_id_fields")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_weather_forecasts")),
    )
    op.create_index(op.f("ix_weather_forecasts_field_id"), "weather_forecasts", ["field_id"], unique=False)
    op.create_index(
        "ix_weather_forecasts_field_event_forecast_date",
        "weather_forecasts",
        ["field_id", "event_type", "forecast_date"],
        unique=True,
    )

    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("alert_id", sa.Integer(), nullable=False),
        sa.Column("forecast_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["alert_id"], ["alerts.id"], name=op.f("fk_notifications_alert_id_alerts")),
        sa.ForeignKeyConstraint(
            ["forecast_id"],
            ["weather_forecasts.id"],
            name=op.f("fk_notifications_forecast_id_weather_forecasts"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_notifications")),
    )
    op.create_index(op.f("ix_notifications_alert_id"), "notifications", ["alert_id"], unique=False)
    op.create_index(op.f("ix_notifications_forecast_id"), "notifications", ["forecast_id"], unique=False)
    op.create_index(
        "ix_notifications_alert_forecast_unique",
        "notifications",
        ["alert_id", "forecast_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("ix_notifications_alert_forecast_unique", table_name="notifications")
    op.drop_index(op.f("ix_notifications_forecast_id"), table_name="notifications")
    op.drop_index(op.f("ix_notifications_alert_id"), table_name="notifications")
    op.drop_table("notifications")

    op.drop_index("ix_weather_forecasts_field_event_forecast_date", table_name="weather_forecasts")
    op.drop_index(op.f("ix_weather_forecasts_field_id"), table_name="weather_forecasts")
    op.drop_table("weather_forecasts")

    op.drop_index("ix_alerts_field_event_active", table_name="alerts")
    op.drop_index(op.f("ix_alerts_field_id"), table_name="alerts")
    op.drop_table("alerts")

    op.drop_index(op.f("ix_fields_user_id"), table_name="fields")
    op.drop_table("fields")

    op.drop_table("users")
