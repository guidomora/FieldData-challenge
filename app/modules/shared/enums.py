from enum import StrEnum


class WeatherEventType(StrEnum):
    FROST = "frost"
    RAIN = "rain"
    HAIL = "hail"
    WIND = "wind"


class NotificationStatus(StrEnum):
    PENDING = "pending"
    SENT = "sent"


class NotificationChannel(StrEnum):
    WHATSAPP = "whatsapp"


class ForecastSource(StrEnum):
    MOCK_INGESTION = "mock_ingestion"
