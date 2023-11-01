from age_timelines.models import AgeEvent, AgeTimeline
from .age import Age
from timelines.pdf.round import Round
from timelines.pdf.scale_description import ScaleDescription, MM_PER_CM


MONTHS_PER_YEAR = 12


class AgeTimelineScaleDescription(ScaleDescription):
    """Class to represent the description of a timeline's scale."""

    def __init__(self, age_timeline: AgeTimeline):
        self.timeline: AgeTimeline = age_timeline

        if self.timeline.ageevent_set.count() > 0:
            self.start_age = self.__youngest_age()
            self.start_age.round_months(Round.DOWN)
            self.start_age.round_years(
                self.timeline.scale_unit, Round.DOWN
            )

            self.end_age = self.__oldest_age()
            self.end_age.round_months(Round.UP)
            self.end_age.round_years(self.timeline.scale_unit, Round.UP)
        else:
            self.start_age = Age(0, 0)
            self.end_age = Age(0, 0)

        self.scale_units: int = self.__scale_units()
        self.scale_length: int = self.__scale_length()

    def __youngest_age(self) -> Age:
        """Finds the youngest age in age_timeline."""
        first_age_event = self.timeline.ageevent_set.first()
        return Age(first_age_event.start_year, first_age_event.start_month)

    def __oldest_age(self) -> Age:
        """Finds the oldest age in age_timeline."""
        last_age_event: AgeEvent = self.timeline.ageevent_set.last()
        oldest_age = Age(last_age_event.start_year, last_age_event.start_month)

        for age_event in self.timeline.ageevent_set.all():
            if age_event.has_end:
                age = Age(age_event.end_year, age_event.end_month)
                if age > oldest_age:
                    oldest_age = age

        return oldest_age

    def __scale_units(self) -> int:
        """Calculate number of scales units needed in timeline scale."""
        years: int = self.end_age.years - self.start_age.years
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
        return str(
            self.start_age.years + (scale_index * self.timeline.scale_unit)
        )

    def plot(self, time_unit) -> float:
        """Calculate in mm where age in months and years should be relative to
        start of timeline scale."""
        years_from_start: float = (
            time_unit.years
            + (time_unit.months / MONTHS_PER_YEAR)
            - self.start_age.years
        )
        scale_units_from_start: float = (
            years_from_start / self.timeline.scale_unit
        )
        distance_from_start: float = (
            scale_units_from_start * self.timeline.scale_length * MM_PER_CM
        )

        return distance_from_start
