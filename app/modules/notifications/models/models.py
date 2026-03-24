from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.modules.shared.enums import NotificationStatus


class Notification(Base):
    __tablename__ = "notifications"
    __table_args__ = (
        Index(
            "ix_notifications_alert_forecast_unique",
            "alert_id",
            "forecast_id",
            unique=True,
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    alert_id: Mapped[int] = mapped_column(ForeignKey("alerts.id"), nullable=False, index=True)
    forecast_id: Mapped[int] = mapped_column(
        ForeignKey("weather_forecasts.id"),
        nullable=False,
        index=True,
    )
    status: Mapped[NotificationStatus] = mapped_column(
        String(30),
        nullable=False,
        default=NotificationStatus.PENDING,
    )
    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    alert = relationship("Alert", back_populates="notifications")
    forecast = relationship("WeatherForecast", back_populates="notifications")

