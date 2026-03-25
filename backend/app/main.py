import logging
import re
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from backend.app.repository import TicketRepository
from backend.app.schemas import HealthResponse
from backend.app.schemas import CreateTicketRequest, TicketResponse


LOGGER_NAME = "challengefreedom.backend"
TICKET_ID_PATTERN = re.compile(r"^TKT-\d+$")


def configure_logging() -> logging.Logger:
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(LOGGER_NAME)


def _unique_fields(
    errors: list[dict],
    *,
    include_types: set[str] | None = None,
    exclude_types: set[str] | None = None,
) -> list[str]:
    fields: list[str] = []
    for error in errors:
        field_name = error["loc"][-1]
        error_type = error["type"]
        if include_types is not None and error_type not in include_types:
            continue
        if exclude_types is not None and error_type in exclude_types:
            continue
        if field_name not in fields:
            fields.append(field_name)
    return fields


def create_app(db_path: str | Path | None = None) -> FastAPI:
    app = FastAPI(title="ChallengeFreedom Support Assistant")
    app.state.logger = configure_logging()
    app.state.ticket_repository = TicketRepository(db_path=db_path)

    @app.exception_handler(RequestValidationError)
    async def handle_request_validation_error(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        errors = exc.errors()
        missing_error_types = {"missing", "string_too_short"}
        missing_fields = _unique_fields(errors, include_types=missing_error_types)
        invalid_fields = _unique_fields(errors, exclude_types=missing_error_types)

        request.app.state.logger.warning(
            "Ticket validation failed: missing_fields=%s invalid_fields=%s",
            missing_fields,
            invalid_fields,
        )
        return JSONResponse(
            status_code=422,
            content={
                "detail": "Missing or invalid ticket data.",
                "missing_fields": missing_fields,
                "invalid_fields": invalid_fields,
            },
        )

    @app.get("/health")
    def read_health() -> HealthResponse:
        return HealthResponse(status="ok")

    @app.get("/tickets/{ticket_id}", response_model=TicketResponse)
    def read_ticket(ticket_id: str) -> TicketResponse:
        app.state.logger.info("Ticket lookup requested for %s", ticket_id)
        if TICKET_ID_PATTERN.fullmatch(ticket_id) is None:
            app.state.logger.warning("Invalid ticket ID format received: %s", ticket_id)
            raise HTTPException(
                status_code=400,
                detail="Invalid ticket ID format. Use TKT-<number>.",
            )

        ticket = app.state.ticket_repository.get_ticket(ticket_id)
        if ticket is None:
            app.state.logger.info("Ticket not found for %s", ticket_id)
            raise HTTPException(status_code=404, detail="Ticket not found.")

        app.state.logger.info("Ticket found for %s", ticket_id)
        return TicketResponse(**ticket)

    @app.post(
        "/tickets",
        response_model=TicketResponse,
        status_code=status.HTTP_201_CREATED,
    )
    def create_ticket(payload: CreateTicketRequest) -> TicketResponse:
        app.state.logger.info("Ticket creation requested")
        ticket = app.state.ticket_repository.create_ticket(
            requester_name=payload.requester_name,
            requester_email=payload.requester_email,
            subject=payload.subject,
            description=payload.description,
        )
        app.state.logger.info("Ticket created with id %s", ticket["id"])
        return TicketResponse(**ticket)

    return app


app = create_app()
