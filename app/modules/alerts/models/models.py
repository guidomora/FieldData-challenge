from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Index, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.modules.shared.enums import WeatherEventType


class Alert(Base):
    __tablename__ = "alerts"
    __table_args__ = (
        Index(
            "ix_alerts_field_event_active",
            "field_id",
            "event_type",
            "is_active",
        ),
        CheckConstraint("threshold >= 0 AND threshold <= 100", name="threshold_range"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    field_id: Mapped[int] = mapped_column(ForeignKey("fields.id"), nullable=False, index=True)
    event_type: Mapped[WeatherEventType] = mapped_column(String(30), nullable=False)
    threshold: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    field = relationship("Field", back_populates="alerts")
    notifications = relationship("Notification", back_populates="alert")

