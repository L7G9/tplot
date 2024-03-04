"""Contains class to describe the layout of timeline on a PDF.

Classes:
    PDFTimelineLayout
"""

from typing import List

from reportlab.lib.units import mm

from timelines.models import Timeline

from .area import Area
from .pdf_event_area import PDFEventArea

A3_LONG = 420 * mm
A3_SHORT = 297 * mm
A4_LONG = 297 * mm
A4_SHORT = 210 * mm
A5_LONG = 210 * mm
A5_SHORT = 148 * mm

DEFAULT_PAGE_BORDER = 10 * mm
DEFAULT_COMPONENT_BORDER = 2 * mm
DEFAULT_EVENT_BORDER = 0.5 * mm


class PDFTimelineLayout:
    """Class to represent the layout of a graphical representation of a
    timeline.

    Uses timeline and scale_description objects to calculate out the size
    of the page needed to display the timeline.
    """

    def __init__(
        self,
        timeline: Timeline,
        page_border=DEFAULT_PAGE_BORDER,
        component_border=DEFAULT_COMPONENT_BORDER,
        event_border=DEFAULT_EVENT_BORDER,
    ):
        self.timeline = timeline
        self.page_border = page_border
        self.component_border = component_border
        self.event_border = event_border

        self.page_area = self.__initial_page_area()
        self.drawable_area: Area = self.__drawable_area(self.page_area)
        self.title_area: Area = Area(0, 0, 0, 0)
        self.description_area: Area = Area(0, 0, 0, 0)
        self.event_and_scale_area: Area = Area(0, 0, 0, 0)
        self.scale_area: Area = Area(0, 0, 0, 0)
        self.event_areas: List[PDFEventArea] = []

    def set_dimensions(
        self, title_height, description_height, scale_width, scale_height
    ):
        """Calculate size and position  all the title, description & scale."""

        if self.timeline.page_orientation == "L":
            self.__landscape_layout(
                title_height, description_height, scale_width, scale_height
            )
        else:
            self.__portrait_layout(
                title_height, description_height, scale_width, scale_height
            )

    def expand_event_overlap(self, max_overlap):
        """Updates areas in layout to take into account extra space required
        for events that overlap the edge of their event areas.
        """
        if self.timeline.page_orientation == "L":
            self.__expand_landscape_layout(max_overlap)
        else:
            self.__expand_portrait_layout(max_overlap)

    def __expand_landscape_layout(self, max_overlap):
        """Updates areas in a landscape layout to take into account extra
        space required for events that overlap the edge of their event areas.
        """
        self.page_area.width += max_overlap
        self.drawable_area.width += max_overlap

    def __expand_portrait_layout(self, max_overlap):
        """Updates areas in a portrait layout to take into account extra space
        required for events that overlap the edge of their event areas.
        """
        self.page_area.height += max_overlap
        self.drawable_area.height += max_overlap
        self.title_area.y += max_overlap
        self.description_area.y += max_overlap
        self.event_and_scale_area.y += max_overlap
        self.scale_area.y += max_overlap
        for event_area in self.event_areas:
            event_area.y += max_overlap

    def __landscape_layout(
        self, title_height, description_height, scale_width, scale_height
    ):
        """Calculate areas for all the elements of the landscape timeline to
        be displayed.
        """
        self.page_area = self.__landscape_page_area(scale_width)
        self.drawable_area = self.__drawable_area(self.page_area)

        self.title_area = self.__title_area(title_height)
        self.description_area = self.__description_area(description_height)
        self.event_and_scale_area = self.__event_and_scale_area()

        event_areas = self.timeline.eventarea_set.all()
        total_weight = self.__total_event_area_weight(event_areas)
        height_per_weight = self.__size_per_weight(
            self.event_and_scale_area.height,
            scale_height,
            event_areas.count(),
            total_weight,
        )
        self.__landscape_event_and_scale_layout(
            height_per_weight, scale_width, scale_height
        )

    def __portrait_layout(
        self, title_height, description_height, scale_width, scale_height
    ):
        """Calculate areas for all the elements of the portrait timeline to be
        displayed.
        """

        self.page_area = self.__portrait_page_area(
            title_height, description_height, scale_height
        )
        self.drawable_area = self.__drawable_area(self.page_area)

        self.title_area = self.__title_area(title_height)
        self.description_area = self.__description_area(description_height)
        self.event_and_scale_area = self.__event_and_scale_area()

        event_areas = self.timeline.eventarea_set.all()
        total_weight = self.__total_event_area_weight(event_areas)
        width_per_weight = self.__size_per_weight(
            self.event_and_scale_area.width,
            scale_width,
            event_areas.count(),
            total_weight,
        )
        self.__portrait_event_and_scale_layout(
            width_per_weight, scale_width, scale_height
        )

    def __initial_page_area(self) -> Area:
        """Calculate an initial area of the PDF which can be used to measure
        text on."""
        # TODO - use something better then "3" & "L"
        if self.timeline.page_orientation == "L":
            if self.timeline.page_size == "3":
                width = A3_LONG
                height = A3_SHORT
            elif self.timeline.page_size == "4":
                width = A4_LONG
                height = A4_SHORT
            else:
                width = A5_LONG
                height = A5_SHORT
        else:
            if self.timeline.page_size == "3":
                width = A3_SHORT
                height = A3_LONG
            elif self.timeline.page_size == "4":
                width = A4_SHORT
                height = A4_LONG
            else:
                width = A5_SHORT
                height = A5_LONG

        return Area(0, 0, width, height)

    def __landscape_page_area(self, scale_width):
        """Calculate area of the whole PDF."""
        scale_width = scale_width + (2 * self.page_border)
        # TODO - use something better then "3"
        if self.timeline.page_size == "3":
            height = A3_SHORT
            width = max(A3_LONG, scale_width)
        elif self.timeline.page_size == "4":
            height = A4_SHORT
            width = max(A4_LONG, scale_width)
        else:
            height = A5_SHORT
            width = max(A5_LONG, scale_width)

        return Area(0, 0, width, height)

    def __portrait_page_area(
        self, title_height, description_height, scale_height
    ) -> Area:
        """Calculate area of the whole PDF."""
        height = (
            title_height
            + description_height
            + scale_height
            + (2 * self.page_border)
            + (2 * self.component_border)
        )
        # TODO - use something better then "3"
        if self.timeline.page_size == "3":
            width = A3_SHORT
        elif self.timeline.page_size == "4":
            width = A4_SHORT
        else:
            width = A5_SHORT

        return Area(0, 0, width, height)

    def __drawable_area(self, page_area: Area) -> Area:
        """Calculate drawable area a border's width inside page_area."""
        return Area(
            self.page_border,
            self.page_border,
            page_area.width - (2 * self.page_border),
            page_area.height - (2 * self.page_border),
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
            self.title_area.y - self.component_border - description_height,
            self.drawable_area.width,
            description_height,
        )

    def __event_and_scale_area(self) -> Area:
        """Calculate combined area for timeline's events and scale between the
        description and the bottom of the drawable area."""
        return Area(
            self.drawable_area.x,
            self.drawable_area.y,
            self.drawable_area.width,
            self.description_area.y
            - self.drawable_area.y
            - self.component_border,
        )

    def __landscape_event_and_scale_layout(
        self, height_per_weight, scale_width, scale_height
    ):
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
                self.scale_area = Area(
                    self.drawable_area.x, next_y, scale_width, scale_height
                )
                next_y += scale_height + self.component_border
                scale_position_calculated = True

            event_area_height = timeline_event_area.weight * height_per_weight
            self.event_areas.append(
                self.__landscape_event_area(
                    next_y, event_area_height, timeline_event_area
                )
            )
            next_y += event_area_height + self.component_border

        if scale_position_calculated is False:
            self.scale_area = Area(
                self.drawable_area.x, next_y, scale_width, scale_height
            )

    def __portrait_event_and_scale_layout(
        self, width_per_weight, scale_width, scale_height
    ):
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
                self.scale_area = Area(
                    next_x, self.drawable_area.y, scale_width, scale_height
                )
                next_x += scale_width + self.component_border
                scale_position_calculated = True

            event_area_width = timeline_event_area.weight * width_per_weight
            self.event_areas.append(
                self.__portrait_event_area(
                    next_x, event_area_width, timeline_event_area
                )
            )
            next_x += event_area_width + self.component_border

        if scale_position_calculated is False:
            self.scale_area = Area(
                next_x, self.drawable_area.y, scale_width, scale_height
            )

    def __landscape_event_area(self, y, height, event_area) -> PDFEventArea:
        """Calculate area for an event area in a landscape timeline."""
        return PDFEventArea(
            self.event_and_scale_area.x,
            y,
            self.event_and_scale_area.width,
            height,
            event_area,
        )

    def __portrait_event_area(self, x, width, event_area) -> PDFEventArea:
        """Calculate area for an event area in a portrait timeline."""
        return PDFEventArea(
            x,
            self.event_and_scale_area.y,
            width,
            self.event_and_scale_area.height,
            event_area,
        )

    def __total_event_area_weight(self, event_areas) -> int:
        """Get total of al event area weights."""
        weight: int = 0

        for event_area in event_areas:
            weight += event_area.weight

        return weight

    def __size_per_weight(
        self, area_size, scale_size, event_area_count, total_weight
    ):
        """Get size (width or height) of a single event area weight."""
        return (
            area_size - scale_size - (event_area_count * self.component_border)
        ) / total_weight
