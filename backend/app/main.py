import logging

from fastapi import FastAPI

from backend.app.schemas import HealthResponse


LOGGER_NAME = "challengefreedom.backend"


def configure_logging() -> logging.Logger:
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(LOGGER_NAME)


def create_app() -> FastAPI:
    app = FastAPI(title="ChallengeFreedom Support Assistant")
    app.state.logger = configure_logging()

    @app.get("/health")
    def read_health() -> HealthResponse:
        return HealthResponse(status="ok")

    return app


app = create_app()
