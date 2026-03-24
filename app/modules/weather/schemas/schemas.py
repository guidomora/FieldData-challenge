from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.modules.shared.enums import ForecastSource, WeatherEventType


class WeatherForecastCreate(BaseModel):
    field_id: int
    event_type: WeatherEventType
    forecast_date: date
    probability: float = Field(ge=0, le=100)
    source: ForecastSource = ForecastSource.MOCK_INGESTION


class WeatherForecastRead(BaseModel):
    id: int
    field_id: int
    event_type: WeatherEventType
    forecast_date: date
    probability: float
    source: ForecastSource
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
