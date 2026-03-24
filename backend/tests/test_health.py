from fastapi.testclient import TestClient

from backend.app.main import create_app


def test_health_returns_ok(tmp_path):
    client = TestClient(create_app(db_path=tmp_path / "support-assistant.db"))

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
