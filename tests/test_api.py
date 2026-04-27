from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


TEST_NOTIFICATION = {
    "user_id": "42",
    "channel": "email",
    "payload": {
        "message": "hello"
    }
}


def test_health():
    response = client.get(
        "/health"
    )

    assert response.status_code == 200
    assert response.json()["api"] == "up"


def test_create_notification():
    response = client.post(
        "/notifications",
        json=TEST_NOTIFICATION
    )

    assert response.status_code == 202
    assert "id" in response.json()


def test_get_notification():
    created = client.post(
        "/notifications",
        json=TEST_NOTIFICATION
    )

    notification_id = created.json()["id"]

    response = client.get(
        f"/notifications/{notification_id}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == notification_id