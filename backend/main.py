from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from loguru import logger

from backend.schemas import CalendarEventRequest, CalendarEventResponse
from backend.services.calendar_service import create_calendar_event

load_dotenv()

app = FastAPI(
    title="Voice Scheduling Agent API",
    description="Backend for a voice-based calendar scheduling agent",
    version="1.0.0"
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/create-calendar-event", response_model=CalendarEventResponse)
def create_event(request: CalendarEventRequest):
    """
    Tool endpoint called by the voice agent after user confirmation.
    Creates a real calendar event.
    """
    try:
        logger.info(
            f"Creating calendar event | "
            f"name={request.name}, date={request.date}, time={request.time}"
        )

        event_id = create_calendar_event(
            name=request.name,
            date=request.date,
            time=request.time,
            title=request.title
        )

        return CalendarEventResponse(
            success=True,
            event_id=event_id,
            message="Calendar event created successfully"
        )

    except Exception as e:
        logger.exception("Failed to create calendar event")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )