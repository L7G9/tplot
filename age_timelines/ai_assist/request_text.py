from timelines.ai_assist.request_text import request_text, StartEndOption


def __get_start_only_age_text() -> str:
    """Describe how an AI should format the age when the user has requested it
    finds events with a start only."""
    return (
        "The start time unit is the age of the topic when the event occurred "
        "using this format 10 Years 3 Months as an example. If no information"
        " about the age that the event occurred is available, the age in "
        " years and months should be calculated by comparing the date event "
        "occurred and the date when the topic started. Leave the end time "
        "unit blank."
    )


def __get_start_end_age_text() -> str:
    """Text describing how an AI should format the age when the user has
    requested it finds events with start & end. If no information about the
    end is available, just the start information is requested."""
    return (
        "If the event occurred over a span of time. The start is the age of"
        " the topic when the event started using this format 10 Years 3 Months"
        " as an example. The end is the age of the topic when the event ended"
        " using the same format. If no information about the start and end age"
        " of the event is available, the age should be should be calculated by"
        " comparing the date event occurred and the date when the topic"
        " started. If no information about the end is available, leave it"
        " blank."
    )


def age_request_text(
    topic: str,
    sources: str,
    count_description: str,
    start_end_option: StartEndOption,
    title_info: str,
    description_info: str,
) -> str:
    """Create a text needed to request that an AI create a list of events
    on a given topic ordered by age."""
    if start_end_option == StartEndOption.USE_START_ONLY:
        time_unit_text = __get_start_only_age_text()
    else:
        time_unit_text = __get_start_end_age_text()

    return request_text(
        topic,
        sources,
        count_description,
        time_unit_text,
        title_info,
        description_info,
    )
