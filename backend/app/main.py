import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException, status

from backend.app.repository import TicketRepository
from backend.app.schemas import HealthResponse
from backend.app.schemas import CreateTicketRequest, TicketResponse


LOGGER_NAME = "challengefreedom.backend"


def configure_logging() -> logging.Logger:
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(LOGGER_NAME)


def create_app(db_path: str | Path | None = None) -> FastAPI:
    app = FastAPI(title="ChallengeFreedom Support Assistant")
    app.state.logger = configure_logging()
    app.state.ticket_repository = TicketRepository(db_path=db_path)

    @app.get("/health")
    def read_health() -> HealthResponse:
        return HealthResponse(status="ok")

    @app.get("/tickets/{ticket_id}", response_model=TicketResponse)
    def read_ticket(ticket_id: str) -> TicketResponse:
        ticket = app.state.ticket_repository.get_ticket(ticket_id)
        if ticket is None:
            raise HTTPException(status_code=404, detail="Ticket not found.")
        return TicketResponse(**ticket)

    @app.post(
        "/tickets",
        response_model=TicketResponse,
        status_code=status.HTTP_201_CREATED,
    )
    def create_ticket(payload: CreateTicketRequest) -> TicketResponse:
        ticket = app.state.ticket_repository.create_ticket(
            requester_name=payload.requester_name,
            requester_email=payload.requester_email,
            subject=payload.subject,
            description=payload.description,
        )
        return TicketResponse(**ticket)

    return app


app = create_app()
