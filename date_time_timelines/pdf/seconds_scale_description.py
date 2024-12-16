from datetime import datetime
from date_time_timelines.models import DateTimeTimeline
from timelines.pdf.scale_description import MM_PER_CM
from .scale_description import DateTimeScaleDescription


class SecondsScaleDescription(DateTimeScaleDescription):
    """Class to represent the description of a DateTimeTimeline's scale when
    it's scale units are in seconds or multiples of seconds including days,
    hours & minutes.

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
        seconds = (
            self.end_date_time.seconds() - self.start_date_time.seconds()
        )
        scale_units: int = seconds // self.timeline.scale_unit

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
        date_time = datetime.fromtimestamp(
            self.start_date_time.date_time.timestamp()
            + (scale_index * self.timeline.scale_unit)
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
        seconds: int = (
            time_unit.seconds() - self.start_date_time.seconds()
        )
        scale_units_from_start: float = seconds / self.timeline.scale_unit

        distance_from_start: float = (
            scale_units_from_start * self.timeline.scale_unit_length * MM_PER_CM
        )
        return distance_from_start
