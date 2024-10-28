from timelines.view_data.timeline_data import TimelineData
from age_timelines.models import AgeEvent, AgeTimeline
from age_timelines.pdf.age import Age
from age_timelines.pdf.age_timeline_scale_description import (
    AgeTimelineScaleDescription
)


class AgeTimelineData(TimelineData):
    """Class to represent the information needed to create a HTML View of an
    age timeline.
    """
    def _create_scale_description(
        self, timeline: AgeTimeline
    ) -> AgeTimelineScaleDescription:
        return AgeTimelineScaleDescription(timeline)

    def _get_events(self, event_area):
        return AgeEvent.objects.filter(event_area=event_area.id)

    def _get_start_time_unit(self, event):
        return Age(event.start_year, event.start_month)

    def _get_end_time_unit(self, event):
        return Age(event.end_year, event.end_month)
