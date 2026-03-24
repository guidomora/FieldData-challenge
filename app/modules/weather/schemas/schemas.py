from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.modules.shared.enums import WeatherEventType


class WeatherForecastCreate(BaseModel):
    field_id: int
    event_type: WeatherEventType
    forecast_date: date
    probability: float = Field(ge=0, le=100)
    source: str = Field(default="mock_ingestion", min_length=1, max_length=100)


class WeatherForecastRead(BaseModel):
    id: int
    field_id: int
    event_type: WeatherEventType
    forecast_date: date
    probability: float
    source: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

