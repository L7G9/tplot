from timelines.ai_assist.request_text import request_text, StartEndOption


def __get_start_only_date_time_text() -> str:
    """Describe how an AI should format the date & time when the user has
    requested it finds events with a start only."""
    return (
        "The start time unit is the date and time that the event occurred in"
        " the format YYYY-MM-DD HH:MM:SS. If no information about the month or"
        " day when the event occurred is available these should be both set to"
        " 01. If no information about the hour, minute or second when the"
        " event occurred is available these should be set to 00. Leave the end"
        " time unit blank."
    )


def __get_start_end_date_time_text() -> str:
    """Text describing how an AI should format the date & time when the user
    has requested it finds events with start & end. If no information about
    the end is available, just the start information is requested."""
    return (
        "If the event occurred over a span of time. The start is the date and"
        " time that the event started in the format YYYY-MM-DD HH:MM:SS. The"
        " end is the date and time that the event ended in the same format. If"
        " no information about the month or day when the event started or"
        " ended is available these should be set to 01. If no information"
        " about the hour, minute or second when the event started or ended is"
        " available these should be set to 00. If no information about the end"
        " is available, leave it blank."
    )


def date_time_request_text(
    topic: str,
    sources: str,
    count_description: str,
    start_end_option: StartEndOption,
    title_info: str,
    description_info: str,
) -> str:
    """Describe a request that an AI create a list of events on a given topic
    ordered by date & time."""
    if start_end_option == StartEndOption.USE_START_ONLY:
        time_unit_text = __get_start_only_date_time_text()
    else:
        time_unit_text = __get_start_end_date_time_text()

    return request_text(
        topic,
        sources,
        count_description,
        time_unit_text,
        title_info,
        description_info
    )
