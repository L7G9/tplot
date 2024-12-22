from abc import ABC, abstractmethod
from timelines.models import Timeline
from timelines.pdf.scale_description import ScaleDescription


MM_PER_CM = 10
START_ONLY_EVENT_MAX_SIZE = 100


class EventData:
    def __init__(
        self, position,
        time,
        title,
        description,
        image,
        tag_string,
        has_end,
        size
    ):
        self.position = position
        self.time = time
        self.title = title
        self.description = description
        self.image = image
        self.tag_string = tag_string
        self.has_end = has_end
        self.size = size


class EventAreaData:
    def __init__(
        self,
        display_event_time,
        display_event_description,
        display_event_image,
        display_event_tags,
        display_event_to_scale_line,
    ):
        self.events = []
        self.display_event_time = display_event_time
        self.display_event_description = display_event_description
        self.display_event_image = display_event_image
        self.display_event_tags = display_event_tags
        self.display_event_to_scale_line = display_event_to_scale_line


class ScaleUnitData:
    def __init__(self, position, unit_string):
        self.position = position
        self.unit_string = unit_string


class TagData:
    def __init__(self, name, description):
        self.name = name
        self.description = description


class TimelineData(ABC):
    """Class to represent the information needed to create a HTML View of a
    timeline.
    """
    def __init__(self, timeline: Timeline):
        scale_description: ScaleDescription = (
            self._create_scale_description(timeline)
        )

        self.title = timeline.title
        self.description = timeline.description
        self.has_description = self.description != ""

        self.event_areas_before_scale = (
            self.get_event_areas(
                self.get_event_areas_before_scale(timeline),
                scale_description
            )
        )
        self.event_areas_after_scale = (
            self.get_event_areas(
                self.get_event_areas_after_scale(timeline),
                scale_description
            )
        )
        self.initial_event_area_width = (
            scale_description.scale_length + START_ONLY_EVENT_MAX_SIZE
        )
        self.start_only_event_max_size = START_ONLY_EVENT_MAX_SIZE

        self.scale_unit_length = scale_description.scale_length
        self.scale_units = self.get_scale_units(scale_description)
        self.scale_unit_max_size = timeline.scale_length * MM_PER_CM

        self.tags = self.get_tags(timeline.tag_set.filter(display=True))
        self.has_tags = len(self.tags) != 0

    @abstractmethod
    def _create_scale_description(
        self, timeline: Timeline
    ) -> ScaleDescription:
        """Creates a ScaleDescription from a Timeline.  Returned object will be
        the subclass of ScaleDescription specific to the type of timeline, eg
        AgeTimelineScaleDescription for AgeTimeline."""
        raise NotImplementedError("Subclasses should implement this")

    def get_event_areas_before_scale(self, timeline):
        return timeline.eventarea_set.filter(
            page_position__lt=timeline.page_scale_position
        )

    def get_event_areas_after_scale(self, timeline):
        return timeline.eventarea_set.filter(
            page_position__gte=timeline.page_scale_position
        )

    @abstractmethod
    def _get_events(self, event_area):
        """Get all events in event area.  Returned list will contain objects
        belonging to a subclass of Event specific to the type of timeline, eg
        AgeEvents for AgeTimeline."""
        raise NotImplementedError("Subclasses should implement this")

    @abstractmethod
    def _get_start_time_unit(self, event):
        """Get start time unit from event.  Returned object will be a subclass
        of TineUnit specific to the type of timeline, eg Age for AgeEvent."""
        raise NotImplementedError("Subclasses should implement this")

    @abstractmethod
    def _get_end_time_unit(self, event):
        """Get end time unit from event.  Returned object will be a subclass
        of TineUnit specific to the type of timeline, eg Age for AgeEvent."""
        raise NotImplementedError("Subclasses should implement this")

    def get_event_area(self, event_area, scale_description):
        event_area_data = EventAreaData(
            event_area.display_event_time,
            event_area.display_event_description,
            event_area.display_event_image,
            event_area.display_event_tags,
            event_area.display_event_to_scale_line,
        )
        events = self._get_events(event_area)
        for event in events:
            start_position = scale_description.plot(
                self._get_start_time_unit(event)
            )

            size = 0
            if event.has_end:
                end_position = scale_description.plot(
                    self._get_end_time_unit(event)
                )
                size = end_position - start_position

            image_url = ""
            if event.image != "":
                image_url = event.image.url

            event_data = EventData(
                position=start_position,
                time=event.time_unit_description(),
                title=event.title,
                description=event.description,
                image=image_url,
                tag_string=event.tag_string(True),
                has_end=event.has_end,
                size=size,
            )
            event_area_data.events.append(event_data)

        return event_area_data

    def get_event_areas(self, event_areas, scale_description):
        event_area_list = []
        for event_area in event_areas:
            event_area_list.append(
                self.get_event_area(event_area, scale_description)
            )

        return event_area_list

    def get_scale_units(self, scale_description):
        scale_units = []
        for unit_index in range(scale_description.get_scale_units() + 1):
            pos = (
                unit_index
                * scale_description.timeline.scale_length
                * MM_PER_CM
            )
            scale_unit = ScaleUnitData(
                pos,
                scale_description.get_scale_label(unit_index)
            )
            scale_units.append(scale_unit)
        return scale_units

    def get_tags(self, tags):
        tag_list = []
        for tag in tags:
            tag_list.append(TagData(tag.name, tag.description))

        return tag_list
