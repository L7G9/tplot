from typing import List

from reportlab.lib.units import mm

from timelines.pdf.pdf_event import PDFEvent
from timelines.pdf.pdf_timeline import PDFTimeline

from ..models import DateTimeEvent, DateTimeTimeline
from .date_time import DateTime
from .scale_description import (
    DateTimeScaleDescription
)
from .years_scale_description import (
    YearsScaleDescription
)
from .months_scale_description import (
    MonthsScaleDescription
)
from .weeks_scale_description import (
    WeeksScaleDescription
)
from .seconds_scale_description import (
    SecondsScaleDescription
)


class PDFDateTimeTimeline(PDFTimeline):
    """Class to draw an DateTimeTimeline on a PDF.

    Extends:
        PDFTimeline
    """

    def __init__(self, date_time_timeline: DateTimeTimeline):
        """Initializes instance.

        Args:
            date_time_timeline: An DateTimeTimeline to create the PDF of.
        """
        PDFTimeline.__init__(self, date_time_timeline)

    def _create_scale_description(
        self, timeline: DateTimeTimeline
    ) -> DateTimeScaleDescription:
        if timeline.is_year_scale_unit():
            return YearsScaleDescription(timeline)
        elif timeline.is_month_scale_unit():
            return MonthsScaleDescription(timeline)
        elif timeline.is_week_scale_unit():
            return WeeksScaleDescription(timeline)
        else:
            return SecondsScaleDescription(timeline)

    def _get_events(self, event_area_id: int) -> List[DateTimeEvent]:
        """Get DateTimeEvents linked to given EventArea in DateTimeTimeline."""
        return DateTimeEvent.objects.filter(event_area=event_area_id)

    def _get_event_start_time(self, event: DateTimeEvent) -> str:
        """Get string describing the time that an AgeEvent with start time
        only occurs."""
        return event.start_date_time.strftime(
            self.timeline.get_event_display_format()
        )

    def _get_event_start_to_end_time(self, event: DateTimeEvent) -> str:
        """Get string describing the time that an AgeEvent with start and end
        time occurs."""
        start_date_time = event.start_date_time.strftime(
            self.timeline.get_event_display_format()
        )
        end_date_time = event.end_date_time.strftime(
            self.timeline.get_event_display_format()
        )
        return f"{start_date_time} to {end_date_time}"

    def _get_event_start_to_end_size(self, event: DateTimeEvent) -> float:
        """Get size (length or height depending on Timeline orientation) that
        an AgeEvent with a start and end time should be on the PDF timeline."""
        start_date_time = DateTime(event.start_date_time)
        end_date_time = DateTime(event.end_date_time)
        size = (
            self.scale.scale_description.plot(end_date_time)
            - self.scale.scale_description.plot(start_date_time)
        ) * mm
        return size

    def _plot_event(self, event: DateTimeEvent, pdf_event: PDFEvent) -> float:
        """Get distance (x or y depending on Timeline orientation) from start
        of Scale that an PDFEvent should be positioned."""
        start_date_time = DateTime(event.start_date_time)
        return self.scale.plot(start_date_time, pdf_event)
