from historical_timelines.models import HistoricalEvent, HistoricalTimeline
from ..historical_year import HistoricalYear
from timelines.pdf.round import Round
from timelines.pdf.scale_description import ScaleDescription, MM_PER_CM


class HistoricalScaleDescription(ScaleDescription):
    """Class to represent the description of a historical timeline's scale."""

    def __init__(self, historical_timeline: HistoricalTimeline):
        ScaleDescription.__init__(self, historical_timeline)

        self.scale_unit = self.timeline.scale_unit

        if self.timeline.historicalevent_set.count() > 0:
            self.start = self.__oldest_historical_year()
            self.start.round(self.timeline.scale_unit, Round.DOWN)

            self.end = self.__newest_historical_year()
            self.end.round(self.timeline.scale_unit, Round.UP)
        else:
            self.start = HistoricalYear(-10)
            self.end = HistoricalYear(10)

        self.scale_units: int = self.__scale_units()
        self.scale_length: int = self.__scale_length()

    def __oldest_historical_year(self) -> HistoricalYear:
        """Finds the oldest historical year in historical_timeline."""
        first_event = self.timeline.historicalevent_set.first()
        return HistoricalYear(first_event.get_start())

    def __newest_historical_year(self) -> HistoricalYear:
        """Finds the latest historical year in historical_timeline."""
        last_event: HistoricalEvent = self.timeline.historicalevent_set.last()
        oldest = HistoricalYear(last_event.get_start())

        for event in self.timeline.historicalevent_set.all():
            if event.has_end:
                historical_year = HistoricalYear(event.get_end())
                if historical_year > oldest:
                    oldest = historical_year

        return oldest

    def __scale_units(self) -> int:
        """Calculate number of scales units needed in timeline scale."""
        years: int = self.end.year - self.start.year
        scale_units: int = years // self.timeline.scale_unit

        if scale_units == 0:
            scale_units = 1

        return scale_units

    def __scale_length(self) -> int:
        """Calculate length of timeline scale in mm."""
        return self.scale_units * self.timeline.scale_length * MM_PER_CM

    def get_scale_units(self) -> int:
        return self.scale_units

    def get_scale_length(self) -> int:
        return self.scale_length

    def get_scale_label(self, scale_index: int) -> str:
        """Get label to got on timeline string."""
        label = HistoricalYear(self.start.year)
        label.year += (scale_index * self.scale_unit)
        return str(label)

    def plot(self, time_unit) -> float:
        """Calculate in mm where the historical year should be relative to
        start of timeline scale."""
        years_from_start: int = time_unit.year - self.start.year
        scale_units_from_start: float = years_from_start / self.scale_unit
        distance_from_start: float = (
            scale_units_from_start * self.timeline.scale_length * MM_PER_CM
        )

        return distance_from_start
