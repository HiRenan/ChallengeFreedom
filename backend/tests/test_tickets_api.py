from fastapi.testclient import TestClient

from backend.app.main import create_app


def test_get_ticket_by_id_returns_existing_ticket():
    client = TestClient(create_app())

    response = client.get("/tickets/TKT-1001")

    assert response.status_code == 200
    assert response.json() == {
        "id": "TKT-1001",
        "requester_name": "Marina Costa",
        "requester_email": "marina.costa@example.com",
        "subject": "Cannot access payroll portal",
        "description": "The payroll portal keeps showing an access denied message.",
        "status": "open",
    }


def test_get_ticket_by_id_returns_custom_404_when_ticket_does_not_exist():
    client = TestClient(create_app())

    response = client.get("/tickets/TKT-9999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found."}


def test_post_tickets_creates_ticket_with_minimum_required_fields():
    client = TestClient(create_app())
    payload = {
        "requester_name": "Ana Silva",
        "requester_email": "ana@example.com",
        "subject": "VPN access issue",
        "description": "I cannot connect to the company VPN since this morning.",
    }

    response = client.post("/tickets", json=payload)

    assert response.status_code == 201
    assert response.json() == {
        "id": "TKT-1002",
        "requester_name": "Ana Silva",
        "requester_email": "ana@example.com",
        "subject": "VPN access issue",
        "description": "I cannot connect to the company VPN since this morning.",
        "status": "open",
    }


def test_post_tickets_returns_default_422_when_required_field_is_missing():
    client = TestClient(create_app())
    payload = {
        "requester_name": "Ana Silva",
        "requester_email": "ana@example.com",
        "subject": "VPN access issue",
    }

    response = client.post("/tickets", json=payload)

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "description"]
