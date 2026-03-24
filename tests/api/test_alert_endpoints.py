import pytest


@pytest.mark.asyncio
async def test_given_seeded_database_when_listing_weather_forecasts_then_endpoint_returns_seeded_rows(
    api_client,
):
    response = await api_client.get("/agrobot/weather-forecasts")

    body = response.json()

    assert response.status_code == 200
    assert len(body) == 6
    assert body[0]["field_id"] == 1


@pytest.mark.asyncio
async def test_given_valid_payload_when_creating_alert_then_endpoint_returns_created_alert(api_client):
    response = await api_client.post(
        "/agrobot/alerts",
        json={"field_id": 1, "event_type": "rain", "threshold": 70},
    )

    body = response.json()

    assert response.status_code == 201
    assert body["field_id"] == 1
    assert body["event_type"] == "rain"
    assert body["threshold"] == 70.0
    assert body["is_active"] is True


@pytest.mark.asyncio
async def test_given_created_alert_when_listing_alerts_then_endpoint_returns_it(api_client):
    create_response = await api_client.post(
        "/agrobot/alerts",
        json={"field_id": 1, "event_type": "rain", "threshold": 70},
    )
    assert create_response.status_code == 201

    list_response = await api_client.get("/agrobot/alerts")

    body = list_response.json()

    assert list_response.status_code == 200
    assert len(body) == 1
    assert body[0]["field_id"] == 1
    assert body[0]["event_type"] == "rain"


@pytest.mark.asyncio
async def test_given_missing_field_when_creating_alert_then_endpoint_returns_business_error(api_client):
    response = await api_client.post(
        "/agrobot/alerts",
        json={"field_id": 999, "event_type": "rain", "threshold": 70},
    )

    assert response.status_code == 400
    assert response.json() == {
        "error": {
            "code": "invalid_alert",
            "message": "Field 999 does not exist.",
        }
    }


@pytest.mark.asyncio
async def test_given_invalid_threshold_type_when_creating_alert_then_endpoint_returns_validation_error(
    api_client,
):
    response = await api_client.post(
        "/agrobot/alerts",
        json={"field_id": 1, "event_type": "rain", "threshold": "high"},
    )

    body = response.json()

    assert response.status_code == 422
    assert body["error"]["code"] == "validation_error"
    assert body["error"]["message"] == "The request contains invalid or missing data."
    assert body["error"]["details"][0]["field"] == "threshold"


@pytest.mark.asyncio
async def test_given_unknown_alert_when_updating_alert_then_endpoint_returns_not_found(api_client):
    response = await api_client.patch(
        "/agrobot/alerts/999",
        json={"threshold": 55},
    )

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "alert_not_found",
            "message": "The requested alert does not exist.",
        }
    }


@pytest.mark.asyncio
async def test_given_matching_alert_when_evaluating_then_notification_is_visible_in_notifications_endpoint(
    api_client,
):
    create_alert_response = await api_client.post(
        "/agrobot/alerts",
        json={"field_id": 1, "event_type": "rain", "threshold": 70},
    )
    assert create_alert_response.status_code == 201

    evaluate_response = await api_client.post("/agrobot/alerts/evaluate")
    notifications_response = await api_client.get("/agrobot/notifications")

    evaluate_body = evaluate_response.json()
    notifications_body = notifications_response.json()

    assert evaluate_response.status_code == 200
    assert evaluate_body["processed_alerts"] == 1
    assert evaluate_body["notifications_created"] == 1
    assert notifications_response.status_code == 200
    assert len(notifications_body) == 1
    assert notifications_body[0]["alert_id"] == create_alert_response.json()["id"]
    assert notifications_body[0]["status"] == "pending"
    assert notifications_body[0]["channel"] == "whatsapp"
    assert notifications_body[0]["recipient"] == "+5491111111111"
