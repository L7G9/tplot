from datetime import datetime
from date_time_timelines.models import DateTimeEvent, DateTimeTimeline
from .date_time import DateTime
from .datetime_utls import (
    get_month_completion,
    round_by_years,
    round_by_months,
    round_by_weeks,
    round_by_seconds
)
from timelines.pdf.round import Round
from timelines.pdf.scale_description import ScaleDescription, MM_PER_CM


class DateTimeScaleDescription(ScaleDescription):
    """Class to represent the description of a DateTimeTimeline's scale.

    Not to be instanced directly but contains common functionality used
    by the different subclasses needed to implement the different scale
    units in a DateTimeTimeline.

    Extends:
        ScaleDescription

    """
    def __init__(self, date_time_timeline: DateTimeTimeline):
        """Initialise Instance.

        Args:
            date_time_timeline: A DateTimeTimeline to build this scale
            description from.
        """
        ScaleDescription.__init__(self, date_time_timeline)

        if self.timeline.datetimeevent_set.count() > 0:
            self.start_date_time: DateTime = self.__first_date_time()
            self.start_date_time.date_time = self.round_datetime(
                self.start_date_time.date_time,
                self.timeline.scale_unit,
                Round.DOWN
            )
            self.end_date_time: DateTime = self.__last_date_time()
            self.end_date_time.date_time = self.round_datetime(
                self.end_date_time.date_time,
                self.timeline.scale_unit,
                Round.UP
            )
        else:
            self.start_date_time = DateTime(datetime.today())
            self.end_date_time = DateTime(datetime.today())

        self.scale_units: int = self._scale_units()
        self.scale_unit_length: int = self.__scale_unit_length()

    def __first_date_time(self) -> DateTime:
        """Finds the first datetime linked to an event in timeline."""
        first_event = self.timeline.datetimeevent_set.first()
        return DateTime(first_event.start_date_time)

    def __last_date_time(self) -> DateTime:
        """Finds the last datetime linked to an event in timeline."""
        last_event: DateTimeEvent = self.timeline.datetimeevent_set.last()
        largest_date_time = DateTime(last_event.start_date_time)

        for date_time_event in self.timeline.datetimeevent_set.all():
            if date_time_event.has_end:
                date_time = DateTime(date_time_event.end_date_time)
                if date_time > largest_date_time:
                    largest_date_time = date_time

        return largest_date_time

    def __scale_unit_length(self) -> int:
        """Calculate length of timeline scale in mm."""
        return self.scale_units * self.timeline.scale_unit_length * MM_PER_CM

    def get_scale_units(self) -> int:
        return self.scale_units

    def get_scale_unit_length(self) -> int:
        return self.scale_unit_length

    def round_datetime(
        self,
        date_time: datetime,
        scale_unit: int,
        round: Round
    ) -> datetime:
        """Round a datetime instance using a scale_unit from a
        DateTimeTimeline.

        Args:
            date_time: A datetime instance to be rounded.
            scale_unit: An int equal to scale_unit from a DateTimeTimeline.
            round: A value of Round enumeration stating to round up or down.

        Returns:
            A datetime instance equal to rounded datetime.
        """

        if self.timeline.is_year_scale_unit():
            year_scale_unit = self.timeline.get_years_in_scale_unit()
            return round_by_years(
                date_time, year_scale_unit, round
            )
        elif self.timeline.is_month_scale_unit():
            month_scale_unit = self.timeline.get_months_in_scale_unit()
            return round_by_months(
                date_time, month_scale_unit, round
            )
        elif self.timeline.is_week_scale_unit():
            return round_by_weeks(date_time, round)
        else:
            return round_by_seconds(date_time, scale_unit, round)

    def get_remaining_scale_units_for_seconds(
        self,
        date_time: datetime,
        months_per_scale_unit: float
    ) -> float:
        """Get how many scale units are in the units smaller than months
        (days, hours, minutes & seconds) in a date_time.

        e.g. if date_time is 2000/11/16 10:00:00 and months_per_scale_unit is
        3, this method returns how many scale unit are in the 16 10:00:00
        portion of date_time.

        Used when plotting events on DateTimeTimelines scaled in months or
        years to work out how far extra along the scale the event should be
        for any remaining days, hours, minutes and seconds.

        Args:
            date_time: A datetime instance to
            months_per_scale_unit: A float equal to number of months in a scale
            unit.

        Returns:
            A float equal to the number of scale units.
        """
        return (
            get_month_completion(date_time) / months_per_scale_unit
        )

    def get_remaining_scale_units_for_months(
        self,
        date_time: datetime,
        months_per_scale_unit: float
    ) -> float:
        """Get how many scale units are in the months of date_time.

        e.g. if date_time is 2000/11/16 10:00:00 and months_per_scale_unit is
        3, this method returns how many scale units are in the 11 portion of
        date_time.

        Used when plotting events on DateTimeTimelines scaled in years to work
        out how far extra along the scale the event should be for any
        remaining months.

        Args:
            date_time: A datetime instance to
            months_per_scale_unit: A float equal to number of months in a scale
            unit.

        Returns:
            A float equal to the number of scale units.
        """
        return (
            (date_time.month - 1) / months_per_scale_unit
        )
