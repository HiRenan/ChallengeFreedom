import logging
import sqlite3

from fastapi.testclient import TestClient

from backend.app.main import create_app


def test_get_ticket_by_id_returns_existing_ticket(tmp_path):
    client = TestClient(create_app(db_path=tmp_path / "support-assistant.db"))

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


def test_get_ticket_by_id_returns_custom_404_when_ticket_does_not_exist(tmp_path):
    client = TestClient(create_app(db_path=tmp_path / "support-assistant.db"))

    response = client.get("/tickets/TKT-9999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found."}


def test_get_ticket_by_id_returns_400_when_ticket_id_format_is_invalid(tmp_path):
    client = TestClient(create_app(db_path=tmp_path / "support-assistant.db"))

    response = client.get("/tickets/abc123")

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid ticket ID format. Use TKT-<number>."
    }


def test_post_tickets_creates_ticket_with_minimum_required_fields(tmp_path):
    client = TestClient(create_app(db_path=tmp_path / "support-assistant.db"))
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


def test_post_tickets_returns_custom_422_when_required_field_is_missing(tmp_path):
    client = TestClient(create_app(db_path=tmp_path / "support-assistant.db"))
    payload = {
        "requester_name": "Ana Silva",
        "requester_email": "ana@example.com",
        "subject": "VPN access issue",
    }

    response = client.post("/tickets", json=payload)

    assert response.status_code == 422
    assert response.json() == {
        "detail": "Missing or invalid ticket data.",
        "missing_fields": ["description"],
        "invalid_fields": [],
    }


def test_post_tickets_returns_custom_422_when_required_field_is_blank(tmp_path):
    client = TestClient(create_app(db_path=tmp_path / "support-assistant.db"))
    payload = {
        "requester_name": "Ana Silva",
        "requester_email": "ana@example.com",
        "subject": "   ",
        "description": "I cannot connect to the company VPN since this morning.",
    }

    response = client.post("/tickets", json=payload)

    assert response.status_code == 422
    assert response.json() == {
        "detail": "Missing or invalid ticket data.",
        "missing_fields": ["subject"],
        "invalid_fields": [],
    }


def test_repository_creates_sqlite_database_and_seeds_once(tmp_path):
    db_path = tmp_path / "support-assistant.db"

    create_app(db_path=db_path)
    create_app(db_path=db_path)

    assert db_path.exists()

    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    row = connection.execute(
        "SELECT COUNT(*) AS count FROM tickets WHERE id = ?",
        ("TKT-1001",),
    ).fetchone()
    connection.close()

    assert row["count"] == 1


def test_post_tickets_persists_ticket_to_sqlite(tmp_path):
    db_path = tmp_path / "support-assistant.db"
    client = TestClient(create_app(db_path=db_path))

    response = client.post(
        "/tickets",
        json={
            "requester_name": "Joao Pereira",
            "requester_email": "joao@example.com",
            "subject": "Email account locked",
            "description": "I need access to my inbox before the afternoon meeting.",
        },
    )

    assert response.status_code == 201
    ticket_id = response.json()["id"]

    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    row = connection.execute(
        "SELECT id, status, created_at FROM tickets WHERE id = ?",
        (ticket_id,),
    ).fetchone()
    connection.close()

    assert row["id"] == ticket_id
    assert row["status"] == "open"
    assert row["created_at"]


def test_lookup_and_creation_emit_operational_logs(tmp_path, caplog):
    client = TestClient(create_app(db_path=tmp_path / "support-assistant.db"))

    with caplog.at_level(logging.INFO, logger="challengefreedom.backend"):
        lookup_response = client.get("/tickets/TKT-1001")
        create_response = client.post(
            "/tickets",
            json={
                "requester_name": "Joao Pereira",
                "requester_email": "joao@example.com",
                "subject": "Email account locked",
                "description": "I need access to my inbox before the afternoon meeting.",
            },
        )

    assert lookup_response.status_code == 200
    assert create_response.status_code == 201
    assert "Ticket lookup requested for TKT-1001" in caplog.text
    assert "Ticket found for TKT-1001" in caplog.text
    assert "Ticket created with id" in caplog.text
