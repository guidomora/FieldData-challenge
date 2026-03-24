from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FieldRead(BaseModel):
    id: int
    user_id: int
    name: str
    location_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

