from timelines.models import Timeline
from .area import Area
from .scale_description import ScaleDescription


A3_LONG = 420
A3_SHORT = 297
A4_LONG = 297
A4_SHORT = 210
A5_LONG = 210
A5_SHORT = 148

DEFAULT_BORDER_SIZE = 10
DEFAULT_SCALE_SIZE = 6
DEFAULT_SCALE_UNIT_LINE_LENGTH = 3


class TimelineLayout:
    """Class to represent the layout of a graphical representation of a
    timeline.

    Uses timeline and scale_description objects to calculate out the size
    of the page needed to display the timeline.
    """

    def __init__(
        self,
        timeline: Timeline,
        scale_description: ScaleDescription,
        border_size=DEFAULT_BORDER_SIZE,
        scale_size=DEFAULT_SCALE_SIZE,
        scale_unit_line_length=DEFAULT_SCALE_UNIT_LINE_LENGTH,
    ):
        self.timeline = timeline
        self.scale_description = scale_description
        self.border_size = border_size
        self.scale_size = scale_size
        self.scale_unit_line_length = scale_unit_line_length

        # TODO - use something better then "L"
        if self.timeline.page_orientation == "L":
            self.page_area = self.__landscape_page_area()
        else:
            self.page_area = self.__portrait_page_area()

        self.drawable_area = self.__drawable_area(self.page_area)

        self.title_area: Area = None
        self.description_area: Area = None
        self.event_and_scale_area: Area = None
        self.scale_area: Area = None
        self.event_areas: [Area] = []

    def create_layout(self, title_height, description_height):
        """Calculate areas for all the elements of the timeline to be
        displayed in mm.
        """

        if self.timeline.page_orientation == "L":
            self.__landscape_layout(title_height, description_height)
        else:
            self.__portrait_layout(title_height, description_height)

    def __landscape_layout(self, title_height, description_height):
        """Calculate areas for all the elements of the timeline to be
        displayed in mm.
        """
        self.title_area = self.__title_area(title_height)
        self.description_area = self.__description_area(description_height)
        self.event_and_scale_area = self.__event_and_scale_area()

        total_weight = self.__total_event_area_weight()

        height_per_weight = self.__size_per_weight(
            self.event_and_scale_area.height, self.scale_size, total_weight
        )
        self.__landscape_event_and_scale_layout(height_per_weight)

    def __portrait_layout(self, title_height, description_height):
        """Calculate areas for all the elements of the timeline to be
        displayed in mm.
        """
        height_increase = title_height + description_height + self.border_size
        self.page_area.height += height_increase
        self.drawable_area.height += height_increase

        self.title_area = self.__title_area(title_height)
        self.description_area = self.__description_area(description_height)
        self.event_and_scale_area = self.__event_and_scale_area(
            description_border=self.border_size
        )

        total_weight = self.__total_event_area_weight()
        width_per_weight = self.__size_per_weight(
            self.event_and_scale_area.width, self.scale_size, total_weight
        )
        self.__portrait_event_and_scale_layout(width_per_weight)

    def __landscape_page_area(self) -> Area:
        """Calculate area of the whole PDF in mm."""
        width = self.scale_description.scale_length + (2 * self.border_size)
        # TODO - use something better then "3"
        if self.timeline.page_size == "3":
            height = A3_SHORT
        elif self.timeline.page_size == "4":
            height = A4_SHORT
        else:
            height = A5_SHORT

        return Area(0, 0, width, height)

    def __portrait_page_area(self) -> Area:
        """Calculate area of the whole PDF in mm."""
        height = self.scale_description.scale_length + (2 * self.border_size)
        # TODO - use something better then "3"
        if self.timeline.page_size == "3":
            width = A3_SHORT
        elif self.timeline.page_size == "4":
            width = A4_SHORT
        else:
            width = A5_SHORT

        return Area(0, 0, width, height)

    def __drawable_area(self, page_area) -> Area:
        """Calculate drawable area a border's width inside page_area in mm."""
        return Area(
            self.border_size,
            self.border_size,
            page_area.width - (2 * self.border_size),
            page_area.height - (2 * self.border_size),
        )

    def __title_area(self, title_height: int) -> Area:
        """Calculate area for timeline's title at the top of the drawable
        area."""
        return Area(
            self.drawable_area.x,
            self.drawable_area.top() - title_height,
            self.drawable_area.width,
            title_height,
        )

    def __description_area(self, description_height: int) -> Area:
        """Calculate area for timeline's description under the title."""
        return Area(
            self.drawable_area.x,
            self.title_area.y - description_height,
            self.drawable_area.width,
            description_height,
        )

    def __event_and_scale_area(self, description_border=0) -> Area:
        """Calculate combined area for timeline's events and scale between the
        description and the bottom of the drawable area."""
        return Area(
            self.drawable_area.x,
            self.drawable_area.y,
            self.drawable_area.width,
            self.description_area.y - self.drawable_area.y - description_border,
        )

    def __landscape_event_and_scale_layout(self, height_per_weight):
        """Calculate areas for each event area and scale in a landscape
        timeline."""
        scale_position_calculated = False
        next_y = self.event_and_scale_area.y

        for timeline_event_area in self.timeline.eventarea_set.all():
            scale_position_reached = (
                self.timeline.page_scale_position
                <= timeline_event_area.page_position
            )
            if (scale_position_calculated is False) and scale_position_reached:
                self.scale_area = self.__landscape_scale_area(next_y)
                next_y += self.scale_size
                scale_position_calculated = True

            event_area_height = timeline_event_area.weight * height_per_weight
            self.event_areas.append(
                self.__landscape_event_area(
                    next_y, event_area_height, timeline_event_area
                )
            )
            next_y += event_area_height

        if scale_position_calculated is False:
            self.scale_area = self.__landscape_scale_area(next_y)

    def __portrait_event_and_scale_layout(self, width_per_weight):
        """Calculate areas for each event area and scale in a portrait
        timeline."""
        scale_position_calculated = False
        next_x = self.event_and_scale_area.x

        for timeline_event_area in self.timeline.eventarea_set.all():
            scale_position_reached = (
                self.timeline.page_scale_position
                <= timeline_event_area.page_position
            )
            if (scale_position_calculated is False) and scale_position_reached:
                self.scale_area = self.__portrait_scale_area(next_x)
                next_x += self.scale_size
                scale_position_calculated = True

            event_area_width = timeline_event_area.weight * width_per_weight
            self.event_areas.append(
                self.__portrait_event_area(
                    next_x, event_area_width, timeline_event_area
                )
            )
            next_x += event_area_width

        if scale_position_calculated is False:
            self.scale_area = self.__portrait_scale_area(next_x)

    def __landscape_scale_area(self, y) -> Area:
        """Calculate area for the scale in a landscape timeline."""
        return Area(
            0,
            y,
            self.page_area.width,
            self.scale_size,
        )

    def __portrait_scale_area(self, x) -> Area:
        """Calculate area for the scale in a portrait timeline."""
        return Area(
            x,
            0,
            self.scale_size,
            self.event_and_scale_area.height + (2 * self.border_size),
        )

    def __landscape_event_area(self, y, height, event_area) -> Area:
        """Calculate area for an event area in a landscape timeline."""
        return Area(
            self.event_and_scale_area.x,
            y,
            self.event_and_scale_area.width,
            height,
            event_area,
        )

    def __portrait_event_area(self, x, width, event_area) -> Area:
        """Calculate area for an event area in a portrait timeline."""
        return Area(
            x,
            self.event_and_scale_area.y,
            width,
            self.event_and_scale_area.height,
            event_area,
        )

    def __total_event_area_weight(self) -> int:
        """Get total of al event area weights."""
        weight: int = 0

        for event_area in self.timeline.eventarea_set.all():
            weight += event_area.weight

        return weight

    def __size_per_weight(self, area_size, scale_size, total_weight):
        """Get size (width or height) of a single event area weight."""
        return (area_size - scale_size) / total_weight
