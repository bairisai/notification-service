from fastapi.testclient import TestClient

from app.common.config import settings
from app.main import app

client = TestClient(app)


def test_submit_notification_returns_202_and_queued() -> None:
    headers = {"X-API-Key": settings.API_KEY}
    payload = {
        "recipient": {"email": "john@example.com", "name": "John Doe"},
        "template": "ORDER_SHIPPED",
        "data": {
            "orderId": "ORD-1001",
            "trackingId": "TRK123456",
            "carrier": "FedEx",
        },
    }

    response = client.post(
        f"{settings.API_PREFIX}/{settings.API_VERSION}/notifications",
        json=payload,
        headers=headers,
    )
    assert response.status_code == 202
    body = response.json()
    assert body["status"] == "QUEUED"
    assert body["message"] == "Notification accepted for processing."
    assert "notification_id" in body


def test_get_notification_status_after_submit() -> None:
    headers = {"X-API-Key": settings.API_KEY}
    payload = {
        "recipient": {"email": "john@example.com", "name": "John Doe"},
        "template": "ORDER_SHIPPED",
        "data": {"orderId": "ORD-1001"},
    }

    post_resp = client.post(
        f"{settings.API_PREFIX}/{settings.API_VERSION}/notifications",
        json=payload,
        headers=headers,
    )
    assert post_resp.status_code == 202

    notification_id = post_resp.json()["notification_id"]
    get_resp = client.get(
        f"{settings.API_PREFIX}/{settings.API_VERSION}/notifications/{notification_id}",
        headers=headers,
    )
    assert get_resp.status_code == 200
    status_body = get_resp.json()
    assert status_body["notification_id"] == notification_id
    assert status_body["status"] == "QUEUED"
