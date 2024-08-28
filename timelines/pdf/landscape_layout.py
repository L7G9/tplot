from timelines.models import Timeline
from .area import Area
from .layout import (
    Layout,
    A3_LONG, A3_SHORT, A4_LONG, A4_SHORT, A5_LONG, A5_SHORT,
    DEFAULT_PAGE_BORDER, DEFAULT_COMPONENT_BORDER, DEFAULT_EVENT_BORDER
)
from .pdf_event_area import PDFEventArea


class LandscapeLayout(Layout):
    """Class to represent the layout of a graphical representation of a
    landscape timeline."""

    def __init__(
        self,
        timeline: Timeline,
        page_border=DEFAULT_PAGE_BORDER,
        component_border=DEFAULT_COMPONENT_BORDER,
        event_border=DEFAULT_EVENT_BORDER,
    ):
        Layout.__init__(
            self,
            timeline,
            page_border,
            component_border,
            event_border
        )

    def _initial_page_area(self, page_size) -> Area:
        """Calculate an initial area of the PDF which can be used to measure
        text on."""
        if page_size == "3":
            width = A3_LONG
            height = A3_SHORT
        elif page_size == "4":
            width = A4_LONG
            height = A4_SHORT
        else:
            width = A5_LONG
            height = A5_SHORT

        return Area(0, 0, width, height)

    def set_dimensions(
        self,
        title_height,
        description_height,
        scale_width,
        scale_height,
        tag_key_height,
    ):
        """Calculate size and position all the graphical components making up
        the pdf timeline."""
        self.page_area = self._page_area(self.timeline.page_size, scale_width)
        self.drawable_area = self._drawable_area(self.page_area)

        self.title_area = self._title_area(title_height)
        self.description_area = self._description_area(description_height)
        self.tag_key_area = self._tag_key_area(tag_key_height)
        self.event_and_scale_area = self._event_and_scale_area()

        event_areas = self.timeline.eventarea_set.all()
        if event_areas.count() > 0:
            total_weight = self._total_event_area_weight(event_areas)
            height_per_weight = self._size_per_weight(
                self.event_and_scale_area.height,
                scale_height,
                event_areas.count(),
                total_weight,
            )
        else:
            height_per_weight = 0

        self._event_and_scale_layout(
            height_per_weight, scale_width, scale_height
        )

    def _page_area(self, page_size, scale_width):
        """Calculate area of the whole PDF."""
        page_width = scale_width + (2 * self.page_border)
        # TODO - use something better then "3"
        if page_size == "3":
            height = A3_SHORT
            width = max(A3_LONG, page_width)
        elif page_size == "4":
            height = A4_SHORT
            width = max(A4_LONG, page_width)
        else:
            height = A5_SHORT
            width = max(A5_LONG, page_width)

        return Area(0, 0, width, height)

    def _event_and_scale_layout(
        self, height_per_weight, scale_width, scale_height
    ):
        """Calculate areas for each event area and scale in a landscape
        timeline."""
        scale_position_calculated = False
        next_y = self.event_and_scale_area.y

        event_areas = (
            self.timeline.eventarea_set.all().order_by('page_position')
        )
        for timeline_event_area in event_areas:
            scale_position_reached = (
                self.timeline.page_scale_position
                <= timeline_event_area.page_position
            )
            if (scale_position_calculated is False) and scale_position_reached:
                self.scale_area = Area(
                    self.event_and_scale_area.x,
                    next_y,
                    scale_width,
                    scale_height
                )
                next_y += scale_height + self.component_border
                scale_position_calculated = True

            event_area_height = timeline_event_area.weight * height_per_weight
            self.event_areas.append(
                self._event_area(
                    next_y, event_area_height, timeline_event_area
                )
            )
            next_y += event_area_height + self.component_border

        if scale_position_calculated is False:
            self.scale_area = Area(
                self.event_and_scale_area.x, next_y, scale_width, scale_height
            )

    def _event_area(self, y, height, event_area) -> PDFEventArea:
        """Calculate area for an event area in a landscape timeline."""
        return PDFEventArea(
            self.event_and_scale_area.x,
            y,
            self.event_and_scale_area.width,
            height,
            event_area,
        )

    def expand_event_overlap(self, max_overlap):
        """Updates areas in layout to take into account extra space required
        for events that overlap the edge of their event areas.
        """
        self.page_area.width += max_overlap
        self.drawable_area.width += max_overlap
