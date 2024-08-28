from scientific_timelines.models import ScientificEvent, ScientificTimeline
from ..scientific_year import ScientificYear
from timelines.pdf.round import Round
from timelines.pdf.scale_description import ScaleDescription, MM_PER_CM


class ScientificScaleDescription(ScaleDescription):
    """Class to represent the description of a scientific timeline's scale."""

    def __init__(self, scientific_timeline: ScientificTimeline):
        ScaleDescription.__init__(self, scientific_timeline)

        self.scale_unit = self.__scale_unit_as_scientific_year(
            self.timeline.scale_unit
        )

        if self.timeline.scientificevent_set.count() > 0:
            self.start = self.__oldest_scientific_year()
            self.start.change_multiplier(self.scale_unit.multiplier)
            self.start.round(self.timeline.scale_unit, Round.DOWN)

            self.end = self.__newest_scientific_year()
            self.end.change_multiplier(self.scale_unit.multiplier)
            self.end.round(self.timeline.scale_unit, Round.UP)
        else:
            self.start = ScientificYear(0, 1000)
            self.end = ScientificYear(0, 1000)

        self.scale_units: int = self.__scale_units()
        self.scale_length: int = self.__scale_length()

    def __scale_unit_as_scientific_year(self, scale_unit) -> ScientificYear:
        if scale_unit <= 50000:
            return ScientificYear(scale_unit / 1000, 1000)
        elif scale_unit <= 50000000:
            return ScientificYear(scale_unit / 1000000, 1000000)
        else:
            return ScientificYear(scale_unit / 1000000000, 1000000000)

    def __oldest_scientific_year(self) -> ScientificYear:
        """Finds the youngest scientific year in scientific_timeline."""
        first_event = self.timeline.scientificevent_set.first()
        return ScientificYear(
            first_event.start_year_fraction, first_event.start_multiplier
        )

    def __newest_scientific_year(self) -> ScientificYear:
        """Finds the oldest scientific year in scientific_timeline."""
        last_event: ScientificEvent = self.timeline.scientificevent_set.last()
        oldest = ScientificYear(
            last_event.start_year_fraction, last_event.start_multiplier
        )

        for event in self.timeline.scientificevent_set.all():
            if event.has_end:
                scientific_year = ScientificYear(
                    event.end_year_fraction, event.end_multiplier
                )
                if scientific_year > oldest:
                    oldest = scientific_year

        return oldest

    def __scale_units(self) -> int:
        """Calculate number of scales units needed in timeline scale."""
        years: int = self.end.years() - self.start.years()
        scale_units: int = int(years // self.timeline.scale_unit)

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
        label = ScientificYear(self.start.fraction, self.start.multiplier)
        label.fraction += scale_index * self.scale_unit.fraction
        return str(label)

    def plot(self, time_unit) -> float:
        """Calculate in mm where the scientific year should be relative to
        start of timeline scale."""
        years_from_start: float = time_unit.years() - self.start.years()
        scale_units_from_start: float = (
            years_from_start / self.scale_unit.years()
        )
        distance_from_start: float = (
            scale_units_from_start * self.timeline.scale_length * MM_PER_CM
        )

        return distance_from_start
