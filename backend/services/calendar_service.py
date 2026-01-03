import os
from datetime import datetime, timedelta
from typing import Optional

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from loguru import logger


SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_calendar_service() -> object:
    """
    Builds and returns an authenticated Google Calendar service.
    """
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        raise RuntimeError("Google Calendar not authenticated. Complete OAuth flow.")

    return build("calendar", "v3", credentials=creds)


def create_calendar_event(
    name: str,
    date: str,
    time: str,
    title: Optional[str] = None
) -> str:
    """
    Creates a real Google Calendar event.
    """

    service = get_calendar_service()

    start_dt = datetime.fromisoformat(f"{date}T{time}")
    end_dt = start_dt + timedelta(minutes=30)

    event = {
        "summary": title or f"Meeting with {name}",
        "description": f"Scheduled by Voice AI Agent for {name}",
        "start": {
            "dateTime": start_dt.isoformat(),
            "timeZone": os.getenv("CALENDAR_TIMEZONE", "Asia/Kolkata"),
        },
        "end": {
            "dateTime": end_dt.isoformat(),
            "timeZone": os.getenv("CALENDAR_TIMEZONE", "Asia/Kolkata"),
        },
    }

    created_event = service.events().insert(
        calendarId="primary",
        body=event
    ).execute()

    event_id = created_event.get("id")

    logger.info(f"Calendar event created: {event_id}")

    return event_id