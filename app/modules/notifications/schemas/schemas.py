from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.modules.shared.enums import NotificationStatus


class NotificationRead(BaseModel):
    id: int
    alert_id: int
    forecast_id: int
    status: NotificationStatus
    message: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

