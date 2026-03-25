import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_DB_PATH = Path("artifacts/runtime/support-assistant.db")


class TicketRepository:
    def __init__(self, db_path: str | Path | None = None) -> None:
        self.storage_name = "tickets"
        resolved = db_path or os.getenv("SUPPORT_ASSISTANT_DB_PATH") or DEFAULT_DB_PATH
        self.db_path = Path(resolved)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_database()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize_database(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS tickets (
                    id TEXT PRIMARY KEY,
                    requester_name TEXT NOT NULL,
                    requester_email TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    description TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            row = connection.execute("SELECT COUNT(*) AS count FROM tickets").fetchone()
            if row["count"] == 0:
                connection.execute(
                    """
                    INSERT INTO tickets (
                        id,
                        requester_name,
                        requester_email,
                        subject,
                        description,
                        status,
                        created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        "TKT-1001",
                        "Marina Costa",
                        "marina.costa@example.com",
                        "VPN access blocked",
                        "I cannot connect to the company VPN since this morning.",
                        "open",
                        "2026-03-24T09:00:00+00:00",
                    ),
                )
            connection.commit()

    def get_ticket(self, ticket_id: str) -> dict | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT id, requester_name, requester_email, subject, description, status, created_at
                FROM tickets
                WHERE id = ?
                """,
                (ticket_id,),
            ).fetchone()
        return dict(row) if row else None

    def create_ticket(
        self,
        *,
        requester_name: str,
        requester_email: str,
        subject: str,
        description: str,
    ) -> dict:
        ticket_id = self._next_ticket_id()
        created_at = datetime.now(timezone.utc).isoformat()
        ticket = {
            "id": ticket_id,
            "requester_name": requester_name,
            "requester_email": requester_email,
            "subject": subject,
            "description": description,
            "status": "open",
            "created_at": created_at,
        }
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO tickets (
                    id,
                    requester_name,
                    requester_email,
                    subject,
                    description,
                    status,
                    created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    ticket["id"],
                    ticket["requester_name"],
                    ticket["requester_email"],
                    ticket["subject"],
                    ticket["description"],
                    ticket["status"],
                    ticket["created_at"],
                ),
            )
            connection.commit()
        return ticket

    def _next_ticket_id(self) -> str:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT id
                FROM tickets
                WHERE id LIKE 'TKT-%'
                ORDER BY CAST(SUBSTR(id, 5) AS INTEGER) DESC
                LIMIT 1
                """
            ).fetchone()
        if row is None:
            return "TKT-1001"
        next_number = int(row["id"].split("-")[1]) + 1
        return f"TKT-{next_number}"
