from datetime import date, datetime

from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, Index, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.modules.shared.enums import ForecastSource, WeatherEventType


class WeatherForecast(Base):
    __tablename__ = "weather_forecasts"
    __table_args__ = (
        Index(
            "ix_weather_forecasts_field_event_forecast_date",
            "field_id",
            "event_type",
            "forecast_date",
            unique=True,
        ),
        CheckConstraint("probability >= 0 AND probability <= 100", name="probability_range"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    field_id: Mapped[int] = mapped_column(ForeignKey("fields.id"), nullable=False, index=True)
    event_type: Mapped[WeatherEventType] = mapped_column(String(30), nullable=False)
    forecast_date: Mapped[date] = mapped_column(Date, nullable=False)
    probability: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    source: Mapped[ForecastSource] = mapped_column(
        String(100),
        nullable=False,
        default=ForecastSource.MOCK_INGESTION,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    field = relationship("Field", back_populates="forecasts")
    notifications = relationship("Notification", back_populates="forecast")
