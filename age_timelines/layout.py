from age_timelines.models import AgeEvent, AgeTimeline
from timelines.models import Timeline


MONTHS_PER_YEAR = 12

MM_PER_CM = 10
A3_LONG = 420
A3_SHORT = 297
A4_LONG = 297
A4_SHORT = 210
A5_LONG = 210
A5_SHORT = 148
BORDER_SIZE = 10
TITLE_SIZE = 20
DESCRIPTION_SIZE = 10
SCALE_SIZE = 15


class Area:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height

    def right(self) -> int:
        return self.x + self.width

    def top(self) -> int:
        return self.y + self.height


class AgeTimelineLayout:
    """Class to represent a layout of a graphical representation of an
    AgeTimeline.

    """

    def __init__(self, age_timeline: AgeTimeline) -> int:
        self.age_timeline: AgeTimeline = age_timeline

        start_months: int = self.get_smallest_age()
        start_year: int = self.get_start_year(start_months)
        self.start_year: int = self.round_year_down(start_year)

        end_months: int = self.get_largest_age()
        end_year: int = self.get_end_year(end_months)
        self.end_year: int = self.round_year_up(end_year)

        self.scale_units: int = self.get_scale_units(
            self.start_year, self.end_year
        )
        self.scale_length: int = self.get_scale_length(
            self.scale_units
        )

        self.page_area = self.get_landscape_page_area()
        self.drawable_area = self.get_drawable_area(
            self.page_area, BORDER_SIZE
        )
        self.title_area: Area = None
        self.description_area: Area = None
        self.timeline_area: Area = None
        self.scale_area: Area = None
        self.event_areas: [Area] = []

    def get_landscape_page_area(self) -> Area:
        """Calculate area of the whole PDF in mm."""
        length = self.scale_length + (2 * BORDER_SIZE)
        if self.age_timeline.page_size == "3":
            height = A3_SHORT
        elif self.age_timeline.page_size == "4":
            height = A4_SHORT
        else:
            height = A5_SHORT

        return Area(0, 0, length, height)

    def get_drawable_area(self, page_area: Area, border_size: int) -> Area:
        """Calculate area inside the border in mm."""
        return Area(
            border_size,
            border_size,
            page_area.width - (2 * border_size),
            page_area.height - (2 * border_size),
        )

    def get_title_area(self, drawable_area: Area, title_height: int) -> Area:
        """Calculate area to display timeline title in mm."""
        return Area(
            drawable_area.x,
            drawable_area.y + drawable_area.height - title_height,
            drawable_area.width,
            title_height,
        )

    def define_title_area(self, title_height: int) -> Area:
        self.title_area = Area(
            self.drawable_area.x,
            self.drawable_area.top() - title_height,
            self.drawable_area.width,
            title_height,
        )
        return self.title_area

    def define_description_area(self, description_height: int) -> Area:
        self.description_area = Area(
            self.drawable_area.x,
            self.title_area.y - description_height,
            self.drawable_area.width,
            description_height,
        )
        return self.description_area

    def define_timeline_area(self) -> Area:
        self.timeline_area = Area(
            self.drawable_area.x,
            self.drawable_area.y,
            self.drawable_area.width,
            self.description_area.y
        )
        return self.timeline_area

    def define_landscape_scale_area(self, y, height) -> Area:
        self.scale_area = Area(
                0
                y,
                self.page_area.width
                height
        )
        return self.scale_area

    def define_landscape_event_area(self, y, height) -> Area:
        event_area = Area(
            self.drawable_area.x,
            y,
            self.drawable_area.width,
            height
        )
        self.event_areas.append(event_area)
        return event_area

    def get_combined_event_area_weights(self) -> int:
        """ """
        weight: int = 0

        for event_area in self.age_timeline.set_eventareas.all():
            weight += event_area.weight

        return weight

    def get_size_per_weight(
        self, area_size, scale_size, combined_weight
    ) -> int:
        return (area_size - scale_size) // combined_weight

    def total_months(self, years: int, months: int) -> int:
        return (years * MONTHS_PER_YEAR) + months

    def start_months(self, age_event: AgeEvent) -> int:
        return self.total_months(age_event.start_year, age_event.start_month)

    def end_months(self, age_event: AgeEvent) -> int:
        return self.total_months(age_event.end_year, age_event.end_month)

    def get_smallest_age(self) -> int:
        """Finds the smallest age in age_timeline.

        This will be start_year and start_month of the 1st AgeEvent in the
        AgeTimeline because they are in ordered by those fields.

        Returns age as the total number of months.
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

    def get_start_year(self, months: int) -> int:
        """Converts months to years rounding down if there are any remaining
        negative months.
        """
        years: int = months // MONTHS_PER_YEAR

        if months % MONTHS_PER_YEAR < 0:
            years -= 1

        return years

    def get_end_year(self, months: int) -> int:
        """Converts months to years rounding up if there are any remaining
        positive months.
        """
        years: int = months // MONTHS_PER_YEAR

        if months % MONTHS_PER_YEAR > 0:
            years += 1

        return years

    def round_year_down(self, year: int) -> int:
        """Rounds year to nearest year on timeline scale."""
        return (
            year // self.age_timeline.scale_unit
        ) * self.age_timeline.scale_unit

    def round_year_up(self, year: int) -> int:
        """Rounds year to nearest year on timeline scale, rounding up if there
        are any remaining years.
        """
        rounded_year: int = self.round_year_down(year)
        remainder: int = year % self.age_timeline.scale_unit

        if remainder != 0:
            rounded_year += self.age_timeline.scale_unit

        return rounded_year

    def get_scale_units(self, start_year: int, end_year: int) -> int:
        """Calculates number of scales units need in timeline scale."""
        years: int = end_year - start_year
        scale_units: int = years // self.age_timeline.scale_unit

        if scale_units == 0:
            scale_units = 1

        return scale_units

    def get_scale_length(self, scale_units: int) -> int:
        """Calculates length of timeline scale in mm."""
        length: int = scale_units * self.age_timeline.scale_length * MM_PER_CM

        return length

    def get_axis_labels(self) -> [(int)]:
        """Make list of year labels to go on timeline scale."""
        list = []
        for scale_unit_count in range(self.scale_units + 1):
            year = self.start_year + (
                scale_unit_count * self.age_timeline.scale_unit
            )
            list.append(year)

        return [tuple(list)]

    def get_scale_label(self, scale_index: int) -> str:
        return str(scale_index * self.age_timeline.scale_unit)

    def plot(self, years, months) -> float:
        """Calculate in mm where age in months and years should be relative to
        start of timeline scale."""
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
