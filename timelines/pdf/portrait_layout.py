from timelines.models import Timeline
from .area import Area
from .layout import (
    Layout,
    A3_LONG, A3_SHORT, A4_LONG, A4_SHORT, A5_LONG, A5_SHORT,
    DEFAULT_PAGE_BORDER, DEFAULT_COMPONENT_BORDER, DEFAULT_EVENT_BORDER
)
from .pdf_event_area import PDFEventArea


class PortraitLayout(Layout):
    """Class to represent the layout of a graphical representation of a
    portrait timeline."""

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

    def _initial_page_area(self, pdf_page_size) -> Area:
        """Calculate an initial area of the PDF which can be used to measure
        text on."""
        if self.timeline.pdf_page_size == "3":
            width = A3_SHORT
            height = A3_LONG
        elif self.timeline.pdf_page_size == "4":
            width = A4_SHORT
            height = A4_LONG
        else:
            width = A5_SHORT
            height = A5_LONG

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
        self.page_area = self._page_area(
            self.timeline.pdf_page_size,
            title_height,
            description_height,
            scale_height,
            tag_key_height
        )
        self.drawable_area = self._drawable_area(self.page_area)

        self.title_area = self._title_area(title_height)
        self.description_area = self._description_area(description_height)
        self.tag_key_area = self._tag_key_area(tag_key_height)
        self.event_and_scale_area = self._event_and_scale_area()

        event_areas = self.timeline.eventarea_set.all()
        if event_areas.count() > 0:
            total_weight = self._total_event_area_weight(event_areas)
            width_per_weight = self._size_per_weight(
                self.event_and_scale_area.width,
                scale_width,
                event_areas.count(),
                total_weight,
            )
        else:
            width_per_weight = 0

        self._event_and_scale_layout(
            width_per_weight, scale_width, scale_height
        )

    def _page_area(
        self,
        pdf_page_size,
        title_height,
        description_height,
        scale_height,
        tag_key_height
    ):
        """Calculate area of the whole PDF."""
        height = (
            title_height
            + description_height
            + scale_height
            + tag_key_height
            + (2 * self.page_border)
            + (3 * self.component_border)
        )
        # TODO - handle case when description  missing / has zero height
        # TODO - handle case when  tag key missing / has zero height
        # TODO - use something better then "3" etc
        if pdf_page_size == "3":
            width = A3_SHORT
        elif pdf_page_size == "4":
            width = A4_SHORT
        else:
            width = A5_SHORT

        return Area(0, 0, width, height)

    def _event_and_scale_layout(
        self, height_per_weight, scale_width, scale_height
    ):
        """Calculate areas for each event area and scale in a portrait
        timeline."""
        scale_position_calculated = False
        next_x = self.event_and_scale_area.x

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
                    next_x,
                    self.event_and_scale_area.y,
                    scale_width,
                    scale_height
                )
                next_x += scale_width + self.component_border
                scale_position_calculated = True

            event_area_width = timeline_event_area.weight * height_per_weight
            self.event_areas.append(
                self._event_area(
                    next_x, event_area_width, timeline_event_area
                )
            )
            next_x += event_area_width + self.component_border

        if scale_position_calculated is False:
            self.scale_area = Area(
                next_x, self.event_and_scale_area.y, scale_width, scale_height
            )

    def _event_area(self, x, width, event_area) -> PDFEventArea:
        """Calculate area for an event area in a portrait timeline."""
        return PDFEventArea(
            x,
            self.event_and_scale_area.y,
            width,
            self.event_and_scale_area.height,
            event_area,
        )

    def expand_event_overlap(self, max_overlap):
        """Updates areas in a portrait layout to take into account extra space
        required for events that overlap the edge of their event areas. """
        self.page_area.height += max_overlap
        self.drawable_area.height += max_overlap
        self.title_area.y += max_overlap
        self.description_area.y += max_overlap
        self.event_and_scale_area.y += max_overlap
        self.scale_area.y += max_overlap
        for event_area in self.event_areas:
            event_area.y += max_overlap
