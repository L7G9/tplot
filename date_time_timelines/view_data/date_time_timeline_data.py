from timelines.view_data.timeline_data import TimelineData
from date_time_timelines.models import DateTimeEvent, DateTimeTimeline
from date_time_timelines.pdf.date_time import DateTime
from date_time_timelines.pdf.scale_description import (
    DateTimeScaleDescription,
)
from date_time_timelines.pdf.years_scale_description import (
    YearsScaleDescription
)
from date_time_timelines.pdf.months_scale_description import (
    MonthsScaleDescription
)
from date_time_timelines.pdf.weeks_scale_description import (
    WeeksScaleDescription
)
from date_time_timelines.pdf.seconds_scale_description import (
    SecondsScaleDescription
)


class DateTimeTimelineData(TimelineData):
    """Class to represent the information needed to create a HTML View of a
    date & time timeline.
    """
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

    def _get_events(self, event_area):
        return DateTimeEvent.objects.filter(event_area=event_area.id)

    def _get_start_time_unit(self, event):
        return DateTime(event.start_date_time)

    def _get_end_time_unit(self, event):
        return DateTime(event.end_date_time)
