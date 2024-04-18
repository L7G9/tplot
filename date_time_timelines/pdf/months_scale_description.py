from datetime import datetime
from date_time_timelines.models import DateTimeTimeline
from timelines.pdf.scale_description import MM_PER_CM
from .scale_description import DateTimeScaleDescription


class MonthsScaleDescription(DateTimeScaleDescription):
    """Class to represent the description of a DateTimeTimeline's scale when
    it's scale units are in months.

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
        months = (
            self.end_date_time.months() - self.start_date_time.months()
        )
        scale_units: int = (
            months // self.timeline.get_months_in_scale_unit()
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
        additional_months = (
            scale_index * self.timeline.get_months_in_scale_unit()
        )
        total_months = (
            self.start_date_time.months() + additional_months
        )
        years_from_start = (total_months // 12) + 1
        months_from_start = (total_months % 12) + 1
        date_time = datetime(
            year=years_from_start,
            month=months_from_start,
            day=1,
        )
        return date_time.strftime(self.timeline.get_scale_display_format())

    # TODO: check if DateTime type can be added to time_unit
    def plot(self, time_unit) -> float:
        """Calculates to scale where along timeline scale time_unit should be
        placed.

        Args:
            time_unit: A ??? instance to position on the scale.

        Returns:
            A float equal to the position along the scale in mm that time_unit
            scale be placed.
        """
        months_from_start: int = (
            time_unit.months() - self.start_date_time.months()
        )
        months_per_scale_unit = self.timeline.get_months_in_scale_unit()

        scale_units_from_start: float = (
            months_from_start / months_per_scale_unit
        )

        scale_units_from_start += self.get_remaining_scale_units_for_seconds(
            time_unit.date_time, months_per_scale_unit
        )

        distance_from_start: float = (
            scale_units_from_start * self.timeline.scale_length * MM_PER_CM
        )
        return distance_from_start
