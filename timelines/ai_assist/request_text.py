from enum import Enum


class StartEndOption(Enum):
    USE_START_ONLY = 1
    USE_END_IF_AVAILABLE = 2


def role_text() -> str:
    """Describe the role an AI should assume when processing the request."""
    return (
        "You are a historical research assistant, skilled at researching "
        "events that happened in relation to any given topic."
    )


def __get_topic_text(topic: str) -> str:
    """Describe the topic of the events an AI should find."""
    return (
        f"Create a list of events containing the {topic}. Each entry in the"
        " list should include four pieces of information, start, end, title"
        " and description.\n"
    )


def __get_source_text(sources: str) -> str:
    """Describe the source URLs an AI should use to find the events find."""
    if sources == "":
        return ""
    else:
        return (
            "Use these URLs as the information source for the events "
            f"{sources}.\n"
        )


def __get_event_count_text(count_description: str) -> str:
    """Describe how many events an AI should attempt to find."""
    if count_description == "":
        return ""
    else:
        return f"Find {count_description} events about the topic.\n"


def __get_title_contents_text(title_info: str) -> str:
    """Describe the contents of the event titles found by an AI."""
    if title_info == "":
        return "The title is a short title of the event.\n"
    else:
        return f"The title is {title_info}.\n"


def __get_description_contents_text(description_info: str) -> str:
    """Describe the contents of the event descriptions found by an AI."""
    if description_info == "":
        return "The description is a short description of the event.\n"
    else:
        return f"The description is {description_info}.\n"


def __get_json_text() -> str:
    """Describe the format of list found by an AI."""
    return (
        "The list must be in JSON format with no other text added.\n"
    )


def request_text(
    topic: str,
    sources: str,
    count_description: str,
    time_unit_text: str,
    title_info: str,
    description_info: str,
) -> str:
    """Describe a request for an AI to find events."""
    return (
        __get_topic_text(topic)
        + __get_source_text(sources)
        + __get_event_count_text(count_description)
        + time_unit_text
        + __get_title_contents_text(title_info)
        + __get_description_contents_text(description_info)
        + __get_json_text()
    )
