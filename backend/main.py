from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from loguru import logger
import os
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
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
    


@app.get("/auth/login")
def google_auth_login():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [os.getenv("GOOGLE_REDIRECT_URI")],
            }
        },
        scopes=["https://www.googleapis.com/auth/calendar"],
    )

    flow.redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    auth_url, _ = flow.authorization_url(prompt="consent")

    return RedirectResponse(auth_url)


@app.get("/auth/callback")
def google_auth_callback(code: str):
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [os.getenv("GOOGLE_REDIRECT_URI")],
            }
        },
        scopes=["https://www.googleapis.com/auth/calendar"],
    )

    flow.redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    flow.fetch_token(code=code)

    with open("token.json", "w") as token:
        token.write(flow.credentials.to_json())

    return {"message": "Google Calendar connected successfully"}
