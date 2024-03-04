"""Contains class to position and draw the events in a timeline's event area
on a canvas.

Classes:
    PDFEventArea
"""

from typing import List, Union

from reportlab.lib.units import mm

from timelines.models import EventArea

from .area import Area
from .inside import Inside
from .pdf_event import PDFEvent


class PDFEventArea(Area):
    """Class representing a Timeline's EventArea on a Canvas.

    Contains the methods to find best position for an Area in this
    instance taking into account it's initial/desired position, it's size and
    this instances's size, other Area instances already positioned in this
    instance and the direction this instance can expand in given the
    orientation of the Timeline.

    Attributes:
        event_area: A EventArea instance this represents on the Canvas.
        events: A list of PDFEvent instances to contained in this area.
    """

    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        event_area: EventArea,
    ):
        """Initialise Instance.

        Args:
            x: A float storing the x coordinate of the Area.
            y: A float storing the y coordinate of the Area.
            width: A float storing the width of the Area.
            height: A float storing the height of the Area.
            event_area: An EventArea instance this will represent on the
            Canvas.
        """
        Area.__init__(self, x, y, width, height)
        self.event_area = event_area
        self.events: List[PDFEvent] = []

    def get_landscape_position(
        self,
        area: Area,
        search_left: bool,
        search_right: bool,
        best_position: Union[tuple[float, float], None] = None,
        gap: float = mm,
    ) -> Union[tuple[float, float], None]:
        """Finds the closest position to the current position of an Area that
        it can be placed in this PDFEventArea instance.

        Tests that the Area fits inside this PDFEventArea or if is does not
        that it only overlaps the right edge of this area with can be expanded.

        Tests that the Area does not overlap any other Areas already in this
        event.  If it does looks for alternative positions where it does not
        overlap any Areas.

        Args:
            event: An Area instance to find the best position for.
            search_left: A bool stating if the space to the left of the event
            argument should be checked.
            search_right: A bool stating if the space to the right of the
            event argument should be checked.
            best_position: A pair of floats storing coordinates of the best
            position found so far.  Is None when no suitable position has
            been found so far.
            gap: A float storing the minimum gap that should be between two
            PDFEvent instances.

        return:
            A pair of floats storing coordinates of the best position found
            for Area. Or None if Area is too big to fit into this instance.
        """
        event_inside = Inside(area, self, True)
        fully_inside = event_inside.test()
        right_outside_only = event_inside.test(right_inside=False)
        if (fully_inside or right_outside_only) is False:
            return best_position

        overlap_area = self.__get_overlapping_area(area)
        if overlap_area is None:
            return area.x, area.y
        else:
            above_area = area.get_area_above(overlap_area, gap)
            best_above_position = self.get_landscape_position(
                above_area, True, True, best_position, gap
            )

            best_left_position = None
            if search_left:
                left_area = area.get_area_to_left(overlap_area, gap)
                best_left_position = self.get_landscape_position(
                    left_area, True, False, best_position, gap
                )

            best_right_position = None
            if search_right:
                right_area = area.get_area_to_right(overlap_area, gap)
                best_right_position = self.get_landscape_position(
                    right_area, False, True, best_position, gap
                )

            updated_best_position = self.__get_best_position(
                (area.x, area.y), best_position, best_above_position, "L"
            )
            updated_best_position = self.__get_best_position(
                (area.x, area.y),
                updated_best_position,
                best_left_position,
                "L",
            )
            updated_best_position = self.__get_best_position(
                (area.x, area.y),
                updated_best_position,
                best_right_position,
                "L",
            )

            return updated_best_position

    def get_portrait_position(
        self,
        area: Area,
        search_above: bool,
        search_below: bool,
        best_position: tuple[float, float] = None,
        gap: float = mm,
    ) -> tuple[float, float]:
        """Finds the closest position to the current position of an Area that
        it can be placed in this PDFEventArea instance.

        Tests that the Area fits inside this PDFEventArea or if is does not
        that it only overlaps the bottom edge of this area with can be
        expanded.

        Tests that the Area does not overlap any other Areas already in this
        event.  If it does looks for alternative positions where it does not
        overlap any Areas.

        Args:
            event: An Area instance to find the best position for.
            search_above: A bool stating if the space above the event argument
            should be checked.
            search_below: A bool stating if the space below the event argument
            should be checked.
            best_position: A pair of floats storing coordinates of the best
            position found so far.  Is None when no suitable position has
            been found so far.
            gap: A float storing the minimum gap that should be between two
            PDFEvent instances.

        return:
            A pair of floats storing coordinates of the best position found
            for Area. Or None if Area is too big to fit into this instance.
        """
        event_inside = Inside(area, self, True)
        fully_inside = event_inside.test()
        bottom_overlap_only = event_inside.test(bottom_inside=False)
        if (fully_inside or bottom_overlap_only) is False:
            return best_position

        overlap_area = self.__get_overlapping_area(area)
        if overlap_area is None:
            return area.x, area.y
        else:
            right_area = area.get_area_to_right(overlap_area, gap)
            best_right_position = self.get_portrait_position(
                right_area, True, True, best_position, gap
            )

            best_above_position = None
            if search_above:
                above_area = area.get_area_above(overlap_area, gap)
                best_above_position = self.get_portrait_position(
                    above_area, True, False, best_position, gap
                )

            best_below_position = None
            if search_below:
                below_area = area.get_area_below(overlap_area, gap)
                best_below_position = self.get_portrait_position(
                    below_area, False, True, best_position, gap
                )

            updated_best_position = self.__get_best_position(
                (area.x, area.y), best_position, best_right_position, "P"
            )
            updated_best_position = self.__get_best_position(
                (area.x, area.y),
                updated_best_position,
                best_above_position,
                "P",
            )
            updated_best_position = self.__get_best_position(
                (area.x, area.y),
                updated_best_position,
                best_below_position,
                "P",
            )

            return updated_best_position

    def __get_overlapping_area(self, area: Area) -> Union[PDFEvent, None]:
        """Gets 1st Area that overlaps with event.

        Assumes Areas already in this PDFEventArea have been positioned in
        order and without overlapping any others.

        Return None is there are no overlapping events."""
        for positioned_event in self.events:
            if area.overlaps(positioned_event):
                return positioned_event

        return None

    def __get_best_position(
        self,
        desired_position: tuple[float, float],
        position1: Union[tuple[float, float], None],
        position2: Union[tuple[float, float], None],
        orientation,
    ) -> Union[tuple[float, float], None]:
        """Get the closest position to desired_position.

        If orientation is landscape this will be the one with the smallest
        horizontal distance to the to the desired_position.
        If orientation is portrait this will be the one with the smallest
        vertical distance to the to the desired_position.
        """
        if desired_position is None:
            raise TypeError(
                "desired_position must be of type (float, float) and not None"
            )

        if (orientation != "L") and (orientation != "P"):
            raise ValueError(
                "orientation must be L for landscape or P for portrait"
            )

        if (position1 is None) and (position2 is None):
            return None

        if position1 is None:
            return position2

        if position2 is None:
            return position1

        if orientation == "L":
            distance1 = abs(desired_position[0] - position1[0])
            distance2 = abs(desired_position[0] - position2[0])
        else:
            distance1 = abs(desired_position[1] - position1[1])
            distance2 = abs(desired_position[1] - position2[1])

        if distance1 < distance2:
            return position1
        else:
            return position2
