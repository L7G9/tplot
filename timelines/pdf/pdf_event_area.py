from typing import List
from reportlab.lib.units import mm
from .area import Area
from .inside import Inside


class PDFEventArea(Area):
    """Class representing an Event Area to be drawn on a Canvas."""

    def __init__(self, x, y, width, height, event_area):
        # replace with
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.event_area = event_area
        self.events: List[Area] = []

    def get_landscape_position(
        self,
        event: Area,
        search_left: bool,
        search_right: bool,
        best_position: (float, float) = None,
        gap: float = mm
    ) -> (float, float):
        """Find position for event in event area after it's position on the
        landscape timeline has been plotted.  Takes into account the size of
        the event area and events that have already been placed in the event
        area.
        """
        event_inside = Inside(event, self, True)
        fully_inside = event_inside.test()
        right_outside_only = event_inside.test(right_inside=False)

        if (fully_inside or right_outside_only) is False:
            return best_position

        overlap_event = self.get_overlapping_event(event)
        if overlap_event is None:
            return event.x, event.y
        else:
            above_area = event.get_area_above(overlap_event, gap)
            best_above_position = self.get_landscape_position(
                above_area, True, True, best_position, gap
            )

            best_left_position = None
            if search_left:
                left_area = event.get_area_to_left(overlap_event, gap)
                best_left_position = self.get_landscape_position(
                    left_area, True, False, best_position, gap
                )
                if (best_left_position is not None):
                    print(f"found right pos {best_left_position}")

            best_right_position = None
            if search_right:
                right_area = event.get_area_to_right(overlap_event, gap)
                best_right_position = self.get_landscape_position(
                    right_area, False, True, best_position, gap
                )
                if (best_right_position is not None):
                    print(f"found right pos {best_right_position}")

            updated_best_position = self.get_best_position(
                (event.x, event.y), best_position, best_above_position, "L"
            )
            updated_best_position = self.get_best_position(
                (event.x, event.y), updated_best_position, best_left_position, "L"
            )
            updated_best_position = self.get_best_position(
                (event.x, event.y), updated_best_position, best_right_position, "L"
            )

            return updated_best_position

    def get_portrait_position(
        self,
        event: Area,
        search_above: bool,
        search_below: bool,
        best_position: (float, float) = None,
        gap: float = mm
    ) -> (float, float):
        """Find position for event in event area after it's position on the
        portrait timeline has been plotted.  Takes into account the size of
        the event area and events that have already been placed in the event
        area.
        """
        print(f"{self}get_portrait_position{event}")
        event_inside = Inside(event, self, True)
        fully_inside = event_inside.test()
        bottom_overlap_only = event_inside.test(bottom_inside=False)

        if (fully_inside or bottom_overlap_only) is False:
            print("event does not fit in event area")
            return best_position

        overlap_event = self.get_overlapping_event(event)
        if overlap_event is None:
            print("no overlaps")
            return event.x, event.y
        else:
            print(f"overlaps{overlap_event}")
            right_area = event.get_area_to_right(overlap_event, gap)
            best_right_position = self.get_portrait_position(
                right_area, True, True, best_position, gap
            )
            if (best_right_position is not None):
                print(f"found right pos {best_right_position}")
            else:
                print("right pos not found")

            best_above_position = None
            if search_above:
                above_area = event.get_area_above(overlap_event, gap)
                best_above_position = self.get_portrait_position(
                    above_area, True, False, best_position, gap
                )
                if (best_above_position is not None):
                    print(f"found above pos {best_above_position}")
                else:
                    print("above pos not found")

            best_below_position = None
            if search_below:
                below_area = event.get_area_below(overlap_event, gap)
                best_below_position = self.get_portrait_position(
                    below_area, False, True, best_position, gap
                )
                if (best_below_position is not None):
                    print(f"found below pos {best_below_position}")
                else:
                    print("below pos not found")

            updated_best_position = self.get_best_position(
                (event.x, event.y), best_position, best_right_position, "P"
            )
            updated_best_position = self.get_best_position(
                (event.x, event.y), updated_best_position, best_above_position, "P"
            )
            updated_best_position = self.get_best_position(
                (event.x, event.y), updated_best_position, best_below_position, "P"
            )

            return updated_best_position

    def get_overlapping_event(self, event: Area):
        """Gets 1st positioned_event that overlaps with event.
        Return None is there are no overlapping events."""
        for positioned_event in self.events:
            if event.overlaps(positioned_event):
                return positioned_event

        return None

    def get_best_position(
        self,
        desired_position: (float, float),
        position1: (float, float),
        position2: (float, float),
        orientation,
    ) -> (float, float):
        """Get the closest position to desired_position."""
        if desired_position is None:
            # TODO throw error
            pass

        # check orientation

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
