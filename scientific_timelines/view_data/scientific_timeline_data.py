from timelines.view_data.timeline_data import TimelineData
from scientific_timelines.models import ScientificEvent, ScientificTimeline
from scientific_timelines.scientific_year import ScientificYear
from scientific_timelines.pdf.scientific_scale_description import (
    ScientificScaleDescription
)


class ScientificTimelineData(TimelineData):
    """Class to represent the information needed to create a HTML View of a
    scientific timeline.
    """
    def _create_scale_description(
        self, timeline: ScientificTimeline
    ) -> ScientificScaleDescription:
        return ScientificScaleDescription(timeline)

    def _get_events(self, event_area):
        return ScientificEvent.objects.filter(event_area=event_area.id)

    def _get_start_time_unit(self, event):
        return ScientificYear(
            event.start_year_fraction, event.start_multiplier
        )

    def _get_end_time_unit(self, event):
        return ScientificYear(event.end_year_fraction, event.end_multiplier)
