"""Contains class for a time unit measured by date and time.

Classes:
    DateTime
"""

from datetime import datetime

from timelines.pdf.time_unit import TimeUnit


class DateTime(TimeUnit):
    """Class for a time unit from a DateTimeTimeline.

    Extends:
        TimeUnit

    Attributes:
        date_time: A datetime instance holding the date and time.
    """
    def __init__(self, date_time: datetime):
        """Initialise Instance.

        Args:
            date_time:
        """
        self.date_time = date_time

    def __str__(self) -> str:
        """Describe this time unit in a string."""
        return str(self.date_time)

    def start_end_string(self, end: "DateTime") -> str:
        """Describe a two time units as a range in a string."""
        return f"{str(self)} to {str(end)}"

    def years(self) -> int:
        """Return total number of whole years in this instance."""
        return self.date_time.year - 1

    def months(self) -> int:
        """Return total number of whole months in this instance."""
        return (self.years() * 12) + (self.date_time.month - 1)

    def seconds(self) -> int:
        """Return total number of whole seconds in this instance."""
        return int(self.date_time.timestamp())

    def __lt__(self, other) -> bool:
        return self.seconds() < other.seconds()

    def __le__(self, other) -> bool:
        return self.seconds() <= other.seconds()

    def __eq__(self, other) -> bool:
        return self.seconds() == other.seconds()

    def __ne__(self, other) -> bool:
        return self.seconds() != other.seconds()

    def __gt__(self, other) -> bool:
        return self.seconds() > other.seconds()

    def __ge__(self, other) -> bool:
        return self.seconds() >= other.seconds()
