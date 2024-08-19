from abc import ABC, abstractmethod
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


class Layout(ABC):
    """Class to represent the layout of a graphical representation of a
    timeline.

    To be implemented by landscape and portrait layouts to represent
    differences due to orientation.
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

        self.page_area = self._initial_page_area(self.timeline.page_size)
        self.drawable_area: Area = self._drawable_area(self.page_area)
        self.title_area: Area = Area(0, 0, 0, 0)
        self.description_area: Area = Area(0, 0, 0, 0)
        self.event_and_scale_area: Area = Area(0, 0, 0, 0)
        self.scale_area: Area = Area(0, 0, 0, 0)
        self.event_areas: List[PDFEventArea] = []
        self.tag_key_area = Area(0, 0, 0, 0)

    @abstractmethod
    def _initial_page_area(self, page_size) -> Area:
        """Calculate an initial area of the PDF which can be used to measure
        text on."""
        raise NotImplementedError("Subclasses should implement this method")

    def _drawable_area(self, page_area: Area) -> Area:
        """Calculate drawable area a border's width inside page_area."""
        return Area(
            self.page_border,
            self.page_border,
            page_area.width - (2 * self.page_border),
            page_area.height - (2 * self.page_border),
        )

    @abstractmethod
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
        raise NotImplementedError("Subclasses should implement this method")

    @abstractmethod
    def _page_area(self, page_size, scale_width):
        """Calculate area of the whole PDF."""
        raise NotImplementedError("Subclasses should implement this method")

    def _title_area(self, title_height: int) -> Area:
        """Calculate area for timeline's title at the top of the drawable
        area."""
        return Area(
            self.drawable_area.x,
            self.drawable_area.top() - title_height,
            self.drawable_area.width,
            title_height,
        )

    def _description_area(self, description_height: int) -> Area:
        """Calculate area for timeline's description under the title."""
        return Area(
            self.drawable_area.x,
            self.title_area.y - self.component_border - description_height,
            self.drawable_area.width,
            description_height,
        )

    def _tag_key_area(self, tag_key_height) -> Area:
        """Calculate area for timeline's tag key at bottom of drawable area.
        """
        return Area(
                self.drawable_area.x,
                self.drawable_area.y,
                self.drawable_area.width,
                tag_key_height,
            )

    def _event_and_scale_area(self) -> Area:
        """Calculate area for scale and all event areas between description
        and tag key."""
        return Area(
            self.drawable_area.x,
            self.tag_key_area.top() + self.component_border,
            self.drawable_area.width,
            (
                self.description_area.y
                - self.tag_key_area.top()
                - (2 * self.component_border)
            ),
        )

    def _event_and_scale_layout(
        self, height_per_weight, scale_width, scale_height
    ):
        """Calculate areas for each event area and scale."""
        raise NotImplementedError("Subclasses should implement this method")

    @abstractmethod
    def _event_area(self, y, height, event_area) -> PDFEventArea:
        """Calculate area for an event area."""
        raise NotImplementedError("Subclasses should implement this method")

    def _total_event_area_weight(self, event_areas) -> int:
        """Get total of al event area weights."""
        weight: int = 0

        for event_area in event_areas:
            weight += event_area.weight

        return weight

    def _size_per_weight(
        self, area_size, scale_size, event_area_count, total_weight
    ):
        """Get size (width or height) of a single event area weight."""
        return (
            area_size - scale_size - (event_area_count * self.component_border)
        ) / total_weight

    def tag_key_column_count(self):
        if self.page_area.width <= A5_SHORT:
            return 1
        elif self.page_area.width <= A5_LONG:
            return 2
        elif self.page_area.width <= A4_LONG:
            return 3
        else:
            return 4

    @abstractmethod
    def expand_event_overlap(self, max_overlap):
        """Updates areas in layout to take into account extra space required
        for events that overlap the edge of their event areas."""
        raise NotImplementedError("Subclasses should implement this method")
