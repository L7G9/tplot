from abc import ABC, abstractmethod


class TimeUnit(ABC):
    """Class to represent a unit of time for a timeline's event.
    """

    @abstractmethod
    def __str__(self) -> str:
        """Describe this time unit as a string."""
        raise NotImplementedError("Subclasses should implement this")

    @abstractmethod
    def start_end_string(self, end: "TimeUnit") -> str:
        """Describe this and end time unit as a string."""
        raise NotImplementedError("Subclasses should implement this")
