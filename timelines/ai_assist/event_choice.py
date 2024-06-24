from typing import List, Dict


class EventChoice:
    """Class to hold details of an event in a format compatible for use with
    form.MultipleChoiceField."""

    def __init__(self, start: str, end: str, title: str, description: str):
        self.start = start
        self.end = end
        self.title = title
        self.description = description

    def __str__(self):
        if self.end == "":
            time = self.start
        else:
            time = f"{self.start} to {self.end}"

        if self.description == "":
            description = "none"
        else:
            description = self.description

        return f"{time} : {self.title} : {description}"


def get_event_choices(
    json_events: List[Dict[str, str, str, str]]
) -> List[EventChoice]:
    """Get list of EventChoice objects from AI JSON output."""
    choices = []
    index = 0
    for event in json_events["events"]:
        choices.append(
            (
                index,
                EventChoice(
                    event["start"],
                    event["end"],
                    event["title"],
                    event["description"],
                ),
            )
        )
        index += 1
    return choices
