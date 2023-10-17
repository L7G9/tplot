from enum import Enum

from age_timelines.models import AgeEvent, AgeTimeline


MONTHS_PER_YEAR = 12
MM_PER_CM = 10


class Round(Enum):
    """Enumeration class to round up or down."""
    UP = 1
    DOWN = 2

    def up(self):
        return self.value == 1

    def down(self):
        return self.value == 2


class ScaleDescription():
    """Class to represent the description of a timeline's scale."""
    def __init__(self, age_timeline: AgeTimeline):
        self.age_timeline: AgeTimeline = age_timeline

        start_months: int = self.get_smallest_age()
        start_year: int = self.months_to_years(start_months, Round.DOWN)
        self.start_year: int = self.nearest_scale_unit(start_year, Round.DOWN)

        end_months: int = self.get_largest_age()
        end_year: int = self.months_to_years(end_months, Round.UP)
        self.end_year: int = self.nearest_scale_unit(end_year, Round.UP)

        self.scale_units: int = self.get_scale_units(
            self.start_year, self.end_year
        )
        self.scale_length: int = self.get_scale_length(
            self.scale_units
        )

    def total_months(self, years: int, months: int) -> int:
        """Calculate the total number of months using units of from an
        AgeEvent.

        AgeTimeline"""
        return (years * MONTHS_PER_YEAR) + months

    def start_months(self, age_event: AgeEvent) -> int:
        """Calculate the total number of months in an AgeEvent's start year
        and month.

        AgeTimeline"""
        return self.total_months(age_event.start_year, age_event.start_month)

    def end_months(self, age_event: AgeEvent) -> int:
        """Calculate the total number of months in an AgeEvent's end year and
        month.

        AgeTimeline"""
        return self.total_months(age_event.end_year, age_event.end_month)

    def get_smallest_age(self) -> int:
        """Finds the smallest age in age_timeline.

        This will be start_year and start_month of the 1st AgeEvent in the
        AgeTimeline because they are in ordered by those fields.

        Returns age as the total number of months.

        AgeTimeline
        """
        # check for timeline with no events
        first_age_event: AgeEvent = self.age_timeline.ageevent_set.first()
        return self.start_months(first_age_event)

    def get_largest_age(self) -> int:
        """Finds the largest age in age_timeline.

        This will be start_year and start_month of the last AgeEvent in the
        AgeTimeline because they are in ordered by those fields OR is the
        largest end_year and end_month of any AgeEvent that uses an end age.

        Returns age as the total number of months.

        AgeTimeline
        """
        # check for timeline with no events
        last_age_event: AgeEvent = self.age_timeline.ageevent_set.last()
        largest_month_total: int = self.start_months(last_age_event)

        for age_event in self.age_timeline.ageevent_set.all():
            if age_event.has_end:
                month_total = self.end_months(age_event)
                if month_total > largest_month_total:
                    largest_month_total = month_total

        return largest_month_total

    def months_to_years(self, months: int, round: Round) -> int:
        """Convert months to years.

        AgeTimeline"""
        years: int = months // MONTHS_PER_YEAR
        remainder = months % MONTHS_PER_YEAR
        if (remainder < 0) and round.down():
            years -= 1
        elif (remainder > 0) and round.up():
            years += 1

        return years

    def nearest_scale_unit(self, years: int, round: Round) -> int:
        """Convert years to nearest number of years on timeline scale.

        AgeTimeline"""
        scale_units = years // self.age_timeline.scale_unit
        remainder = years % self.age_timeline.scale_unit
        if (remainder < 0) and round.down():
            scale_units -= 1
        elif (remainder > 0) and round.up():
            scale_units += 1

        return scale_units * self.age_timeline.scale_unit

    def get_scale_units(self, start_year: int, end_year: int) -> int:
        """Calculates number of scales units need in timeline scale.

        AgeTimeline"""
        years: int = end_year - start_year
        scale_units: int = years // self.age_timeline.scale_unit

        if scale_units == 0:
            scale_units = 1

        return scale_units

    def get_scale_length(self, scale_units: int) -> int:
        """Calculates length of timeline scale in mm.

        Timeline"""
        length: int = scale_units * self.age_timeline.scale_length * MM_PER_CM

        return length

    def get_scale_label(self, scale_index: int) -> str:
        """Get label to got on timeline string.

        AgeTimeline"""
        return str(
            self.start_year + (scale_index * self.age_timeline.scale_unit)
        )

    def plot(self, years, months) -> float:
        """Calculate in mm where age in months and years should be relative to
        start of timeline scale.

        AgeTimeline"""
        years_from_start: float = (
            years + (months / MONTHS_PER_YEAR) - self.start_year
        )
        scale_units_from_start: float = (
            years_from_start / self.age_timeline.scale_unit
        )
        distance_from_start: float = (
            scale_units_from_start * self.age_timeline.scale_length * MM_PER_CM
        )

        return distance_from_start
