from loguru import logger


def create_calendar_event(name: str, date: str, time: str, title: str | None = None) -> str:
    """
    Temporary stub for calendar event creation.
    This will be replaced with real Google Calendar integration.
    """
    logger.info(
        f"[STUB] Creating calendar event | "
        f"name={name}, date={date}, time={time}, title={title}"
    )

    # Return a fake event ID for now
    return "dummy-event-id"