from pydantic import BaseModel, Field
from typing import Optional


class CalendarEventRequest(BaseModel):
    name: str = Field(..., description="Name of the user")
    date: str = Field(
        ...,
        description="Meeting date in ISO format (YYYY-MM-DD)"
    )
    time: str = Field(
        ...,
        description="Meeting time in 24-hour format (HH:MM)"
    )
    title: Optional[str] = Field(
        default=None,
        description="Optional meeting title"
    )


class CalendarEventResponse(BaseModel):
    success: bool
    event_id: Optional[str] = None
    message: str