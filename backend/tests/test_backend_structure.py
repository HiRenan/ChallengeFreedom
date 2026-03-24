from backend.app.main import create_app
from backend.app.repository import TicketRepository
from backend.app.schemas import HealthResponse


def test_backend_internal_modules_exist_and_are_wired():
    app = create_app()
    payload = HealthResponse(status="ok")
    repository = TicketRepository()

    assert payload.model_dump() == {"status": "ok"}
    assert repository is not None
    assert app.state.logger.name == "challengefreedom.backend"
