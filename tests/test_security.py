from fastapi.testclient import TestClient

from app.common.config import settings
from app.main import app

client = TestClient(app)


def test_missing_api_key_returns_401() -> None:
    payload = {
        "recipient": {"email": "john@example.com", "name": "John Doe"},
        "template": "ORDER_SHIPPED",
        "data": {"orderId": "ORD-1001"},
    }

    response = client.post(
        f"{settings.API_PREFIX}/{settings.API_VERSION}/notifications",
        json=payload,
    )
    assert response.status_code == 401
