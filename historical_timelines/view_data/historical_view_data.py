from timelines.view_data.timeline_data import TimelineData
from historical_timelines.models import HistoricalEvent, HistoricalTimeline
from historical_timelines.historical_year import HistoricalYear
from historical_timelines.pdf.historical_scale_description import (
    HistoricalScaleDescription
)


class HistoricalTimelineData(TimelineData):
    """Class to hold the data needed to create a view of a historical
    timeline.
    """
    def _create_scale_description(
        self, timeline: HistoricalTimeline
    ) -> HistoricalScaleDescription:
        return HistoricalScaleDescription(timeline)

    def _get_events(self, event_area):
        return HistoricalEvent.objects.filter(event_area=event_area.id)

    def _get_start_time_unit(self, event):
        return HistoricalYear(event.start_bc_ad * event.start_year)

    def _get_end_time_unit(self, event):
        return HistoricalYear(event.end_bc_ad * event.end_year)
