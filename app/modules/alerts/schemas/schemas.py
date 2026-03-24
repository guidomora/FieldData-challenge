from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.modules.shared.enums import WeatherEventType


class AlertCreate(BaseModel):
    field_id: int
    event_type: WeatherEventType
    threshold: float = Field(ge=0, le=100)


class AlertUpdate(BaseModel):
    threshold: float | None = Field(default=None, ge=0, le=100)
    is_active: bool | None = None


class AlertRead(BaseModel):
    id: int
    field_id: int
    event_type: WeatherEventType
    threshold: float
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AlertEvaluationSummary(BaseModel):
    processed_alerts: int
    notifications_created: int
