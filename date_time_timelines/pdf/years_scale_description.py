from datetime import datetime
from date_time_timelines.models import DateTimeTimeline
from timelines.pdf.scale_description import MM_PER_CM
from .scale_description import (
    DateTimeScaleDescription
)


class YearsScaleDescription(DateTimeScaleDescription):
    """Class to represent the description of a DateTimeTimeline's scale when
    it's scale units are in years.

    Extends:
        DateTimeTimelineScaleDescription
    """
    def __init__(self, date_time_timeline: DateTimeTimeline):
        """Initialise Instance.

        Args:
            date_time_timeline: A DateTimeTimeline to build this scale
            description from.
        """
        DateTimeScaleDescription.__init__(self, date_time_timeline)

    def _scale_units(self) -> int:
        """Calculate number of scale units long the scale should be to fit
        all events in the timeline.

        Returns:
            An int equal to the number of scale units.
        """
        years = self.end_date_time.years() - self.start_date_time.years()
        scale_units: int = (
            years // self.timeline.get_years_in_scale_unit()
        )
        if scale_units == 0:
            scale_units = 1
        return scale_units

    def get_scale_label(self, scale_index: int) -> str:
        """Get label to got on timeline scale.

        Args:
            scale_index: A int equal to the nth scale_unit along the
            timeline's scale.
        Returns:
            A string describing the nth label on the scale.
        """
        years_from_start = (
            scale_index * self.timeline.get_years_in_scale_unit()
        )
        date_time = datetime(
            year=self.start_date_time.years() + 1 + years_from_start,
            month=1,
            day=1,
        )
        return date_time.strftime(self.timeline.get_scale_display_format())

    def plot(self, time_unit) -> float:
        """Calculates to scale where along timeline scale time_unit should be
        placed.

        Args:
            time_unit: A ??? instance to position on the scale.

        Returns:
            A float equal to the position along the scale in mm that time_unit
            scale be placed.
        """
        years_from_start: int = (
            time_unit.years() - self.start_date_time.years()
        )
        years_per_scale_unit = self.timeline.get_years_in_scale_unit()
        scale_units_from_start: float = (
            years_from_start
            / years_per_scale_unit
        )

        months_per_scale_unit = years_per_scale_unit * 12
        scale_units_from_start += self.get_remaining_scale_units_for_months(
            time_unit.date_time, months_per_scale_unit
        )
        scale_units_from_start += self.get_remaining_scale_units_for_seconds(
            time_unit.date_time, months_per_scale_unit
        )

        distance_from_start: float = (
            scale_units_from_start * self.timeline.scale_length * MM_PER_CM
        )
        return distance_from_start
