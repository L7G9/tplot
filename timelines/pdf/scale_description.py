from abc import ABC, abstractmethod


MM_PER_CM = 10


class ScaleDescription(ABC):
    """Class to represent the description of a timeline's scale."""

    @abstractmethod
    def get_scale_units(self) -> int:
        """Calculates number of scales units needed in timeline scale."""
        raise NotImplementedError("Subclasses should implement this")

    @abstractmethod
    def get_scale_length(self) -> int:
        """Calculates length of timeline scale in mm."""
        raise NotImplementedError("Subclasses should implement this")

    @abstractmethod
    def get_scale_label(self, scale_index: int) -> str:
        """Calculates length of timeline scale in mm."""
        raise NotImplementedError("Subclasses should implement this")

    @abstractmethod
    def plot(self, time_unit) -> float:
        """Calculates length of timeline scale in mm."""
        raise NotImplementedError("Subclasses should implement this")
