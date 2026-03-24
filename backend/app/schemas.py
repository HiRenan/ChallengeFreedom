from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class CreateTicketRequest(BaseModel):
    requester_name: str
    requester_email: str
    subject: str
    description: str


class TicketResponse(BaseModel):
    id: str
    requester_name: str
    requester_email: str
    subject: str
    description: str
    status: str
