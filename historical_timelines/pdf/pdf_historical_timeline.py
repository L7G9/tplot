"""Contains class to turn an HistoricalTimeline into a PDF.

Classes:
    PDFHistoricalTimeline
"""

from typing import List

from reportlab.lib.units import mm

from timelines.pdf.pdf_event import PDFEvent
from timelines.pdf.pdf_timeline import PDFTimeline

from ..models import HistoricalEvent, HistoricalTimeline
from ..historical_year import HistoricalYear
from .historical_scale_description import HistoricalScaleDescription


class PDFHistoricalTimeline(PDFTimeline):
    """Class to draw a HistoricalTimeline on a PDF.

    Extends:
        PDFTimeline
    """

    def __init__(self, historical_timeline: HistoricalTimeline):
        """Initializes instance.

        Args:
            historical_timeline: An HistoricalTimeline to create the PDF of.
        """
        PDFTimeline.__init__(self, historical_timeline)

    def _create_scale_description(
        self, timeline: HistoricalTimeline
    ) -> HistoricalScaleDescription:
        return HistoricalScaleDescription(timeline)

    def _get_events(self, event_area_id: int) -> List[HistoricalEvent]:
        """Get HistoricalEvents linked to given EventArea in
        HistoricalTimeline."""
        return HistoricalEvent.objects.filter(event_area=event_area_id)

    def _get_event_start_time(self, event: HistoricalEvent) -> str:
        """Get string describing the time that an HistoricalEvent with start
        only occurs."""
        start = HistoricalYear(event.get_start())
        return str(start)

    def _get_event_start_to_end_time(self, event: HistoricalEvent) -> str:
        """Get string describing the time that an HistoricalEvent with start
        and end occurs."""
        start = HistoricalYear(event.get_start())
        end = HistoricalYear(event.get_end())
        return start.start_end_string(end)

    def _get_event_start_to_end_size(self, event: HistoricalEvent) -> float:
        """Get size (length or height depending on Timeline orientation) that
        an HistoricalEvent with a start and end should be on the PDF timeline.
        """
        start = HistoricalYear(event.get_start())
        end = HistoricalYear(event.get_end())
        size = (
            self.scale.scale_description.plot(end)
            - self.scale.scale_description.plot(start)
        ) * mm
        return size

    def _plot_event(
        self,
        event: HistoricalEvent,
        pdf_event: PDFEvent
    ) -> float:
        """Get distance (x or y depending on Timeline orientation) from start
        of Scale that an PDFEvent should be positioned."""
        start = HistoricalYear(event.get_start())
        return self.scale.plot(start, pdf_event)
