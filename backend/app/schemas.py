from typing import Annotated

from pydantic import BaseModel, StringConstraints


RequiredText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class HealthResponse(BaseModel):
    status: str


class CreateTicketRequest(BaseModel):
    requester_name: RequiredText
    requester_email: RequiredText
    subject: RequiredText
    description: RequiredText


class TicketResponse(BaseModel):
    id: str
    requester_name: str
    requester_email: str
    subject: str
    description: str
    status: str
