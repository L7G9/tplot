"""Contains class to turn an ScientificTimeline into a PDF.

Classes:
    PDFScientificTimeline
"""

from typing import List

from reportlab.lib.units import mm

from timelines.pdf.pdf_event import PDFEvent
from timelines.pdf.pdf_timeline import PDFTimeline

from ..models import ScientificEvent, ScientificTimeline
from ..scientific_year import ScientificYear
from .scientific_scale_description import ScientificScaleDescription


class PDFScientificTimeline(PDFTimeline):
    """Class to draw an ScientificTimeline on a PDF.

    Extends:
        PDFTimeline
    """

    def __init__(self, scientific_timeline: ScientificTimeline):
        """Initializes instance.

        Args:
            scientific_timeline: An ScientificTimeline to create the PDF of.
        """
        PDFTimeline.__init__(self, scientific_timeline)

    def _create_scale_description(
        self, timeline: ScientificTimeline
    ) -> ScientificScaleDescription:
        return ScientificScaleDescription(timeline)

    def _get_events(self, event_area_id: int) -> List[ScientificEvent]:
        """Get ScientificEvents linked to given EventArea in
        ScientificTimeline."""
        return ScientificEvent.objects.filter(event_area=event_area_id)

    def _get_event_start_time(self, event: ScientificEvent) -> str:
        """Get string describing the time that an ScientificEvent with start
        only occurs."""
        start = ScientificYear(
            event.start_year_fraction,
            event.start_multiplier,
        )
        return str(start)

    def _get_event_start_to_end_time(self, event: ScientificEvent) -> str:
        """Get string describing the time that an ScientificEvent with start
        and end occurs."""
        start = ScientificYear(
            event.start_year_fraction,
            event.start_multiplier,
        )
        end = ScientificYear(
            event.end_year_fraction,
            event.end_multiplier,
        )
        return start.start_end_string(end)

    def _get_event_start_to_end_size(self, event: ScientificEvent) -> float:
        """Get size (length or height depending on Timeline orientation) that
        an ScientificEvent with a start and end should be on the PDF timeline.
        """
        start = ScientificYear(
            event.start_year_fraction, event.start_multiplier
        )
        end = ScientificYear(
            event.end_year_fraction,
            event.end_multiplier,
        )
        size = (
            self.scale.scale_description.plot(end)
            - self.scale.scale_description.plot(start)
        ) * mm
        return size

    def _plot_event(
        self, event: ScientificEvent, pdf_event: PDFEvent
    ) -> float:
        """Get distance (x or y depending on Timeline orientation) from start
        of Scale that an PDFEvent should be positioned."""
        start = ScientificYear(
            event.start_year_fraction, event.start_multiplier
        )
        return self.scale.plot(start, pdf_event)
