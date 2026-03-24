class TicketRepository:
    def __init__(self) -> None:
        self.storage_name = "tickets"
        self._tickets = {
            "TKT-1001": {
                "id": "TKT-1001",
                "requester_name": "Marina Costa",
                "requester_email": "marina.costa@example.com",
                "subject": "Cannot access payroll portal",
                "description": "The payroll portal keeps showing an access denied message.",
                "status": "open",
            }
        }
        self._next_id = 1002

    def get_ticket(self, ticket_id: str) -> dict | None:
        return self._tickets.get(ticket_id)

    def create_ticket(
        self,
        *,
        requester_name: str,
        requester_email: str,
        subject: str,
        description: str,
    ) -> dict:
        ticket_id = f"TKT-{self._next_id}"
        self._next_id += 1
        ticket = {
            "id": ticket_id,
            "requester_name": requester_name,
            "requester_email": requester_email,
            "subject": subject,
            "description": description,
            "status": "open",
        }
        self._tickets[ticket_id] = ticket
        return ticket
