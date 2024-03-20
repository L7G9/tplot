"""Contains class to turn an AgeTimeline into a PDF.

Classes:
    PDFAgeTimeline
"""

from typing import List

from reportlab.lib.units import mm

from timelines.pdf.pdf_event import PDFEvent
from timelines.pdf.pdf_timeline import PDFTimeline

from ..models import AgeEvent, AgeTimeline
from .age import Age
from .age_timeline_scale_description import AgeTimelineScaleDescription


class PDFAgeTimeline(PDFTimeline):
    """Class to draw an AgeTimeline on a PDF.

    Extends:
        PDFTimeline
    """

    def __init__(self, age_timeline: AgeTimeline):
        """Initializes instance.

        Args:
            age_timeline: An AgeTimeline to create the PDF of.
        """
        PDFTimeline.__init__(self, age_timeline)

    def _create_scale_description(
        self, timeline: AgeTimeline
    ) -> AgeTimelineScaleDescription:
        return AgeTimelineScaleDescription(timeline)

    def _get_events(self, event_area_id: int) -> List[AgeEvent]:
        """Get AgeEvents linked to given EventArea in AgeTimeline."""
        return AgeEvent.objects.filter(event_area=event_area_id)

    def _get_event_start_time(self, event: AgeEvent) -> str:
        """Get string describing the time that an AgeEvent with start time
        only occurs."""
        start_age = Age(int(event.start_year), int(event.start_month))
        return str(start_age)

    def _get_event_start_to_end_time(self, event: AgeEvent) -> str:
        """Get string describing the time that an AgeEvent with start and end
        time occurs."""
        start_age = Age(event.start_year, event.start_month)
        end_age = Age(event.end_year, event.end_month)
        return start_age.start_end_string(end_age)

    def _get_event_start_to_end_size(self, event: AgeEvent) -> float:
        """Get size (length or height depending on Timeline orientation) that
        an AgeEvent with a start and end time should be on the PDF timeline."""
        start_age = Age(event.start_year, event.start_month)
        end_age = Age(event.end_year, event.end_month)
        size = (
            self.scale.scale_description.plot(end_age)
            - self.scale.scale_description.plot(start_age)
        ) * mm
        return size

    def _plot_event(self, event: AgeEvent, pdf_event: PDFEvent) -> float:
        """Get distance (x or y depending on Timeline orientation) from start
        of Scale that an PDFEvent should be positioned."""
        start_age = Age(event.start_year, event.start_month)
        return self.scale.plot(start_age, pdf_event)
