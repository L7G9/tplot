from age_timelines.models import AgeTimeline
from .area import Area
from .scale_description import ScaleDescription

A3_LONG = 420
A3_SHORT = 297
A4_LONG = 297
A4_SHORT = 210
A5_LONG = 210
A5_SHORT = 148
BORDER_SIZE = 10
TITLE_SIZE = 20
DESCRIPTION_SIZE = 10
SCALE_SIZE = 6
SCALE_UNIT_LINE_LENGTH = 3


class AgeTimelineLayout:
    """Class to represent a layout of a graphical representation of an
    AgeTimeline.
    """
    def __init__(self, age_timeline: AgeTimeline) -> int:
        self.age_timeline: AgeTimeline = age_timeline

        self.scale_description = ScaleDescription(age_timeline)

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
        length = self.scale_description.scale_length + (2 * BORDER_SIZE)
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
            self.description_area.y - self.drawable_area.y,
        )
        return self.timeline_area

    def define_landscape_scale_area(self, y, height) -> Area:
        self.scale_area = Area(0, y, self.page_area.width, height)
        return self.scale_area

    def define_landscape_event_area(self, y, height, event_area) -> Area:
        event_area = Area(
            self.drawable_area.x,
            y,
            self.drawable_area.width,
            height,
            event_area
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
