"""Contains class for a rectangular area.

Classes:
    Area
"""


class Area():
    """Class to represent a rectangular area.

    Attributes:
        x: A float storing the x coordinate of the Area.
        y: A float storing the y coordinate of the Area.
        width: A float storing the width of the Area.
        height: A float storing the height of the Area.
    """

    def __init__(self, x: float, y: float, width: float, height: float):
        """Initialise Instance.

        Args:
            x: A float storing the x coordinate of the Area.
            y: A float storing the y coordinate of the Area.
            width: A float storing the width of the Area.
            height: A float storing the height of the Area.
        """
        self.x: float = x
        self.y: float = y
        self.width: float = width
        self.height: float = height

    def copy_coordinates(self, area: "Area"):
        """Copy x and y coordinates from argument Area to this Area.

        Args:
            area: An Area to copy the coordinates from.
        """
        self.x = area.x
        self.y = area.y

    def copy_dimensions(self, area: "Area"):
        """Copy width and height from argument Area to this Area.

        Args:
            area: An Area to copy the dimensions from.
        """
        self.width = area.width
        self.height = area.height

    def copy(self, area: "Area"):
        """Copy coordinates and dimensions from argument Area to this Area.

        Args:
            area: An Area to copy the coordinates and dimensions from.
        """
        self.copy_coordinates(area)
        self.copy_dimensions(area)

    def right(self) -> float:
        """Get x coordinate of the right most edge of this Area.

        Returns:
            A float containing x coordinate.
        """
        return self.x + self.width

    def top(self) -> float:
        """Get y coordinate of the top most edge of this Area.

        Returns:
            A float containing x coordinate.
        """
        return self.y + self.height

    def inside(self, area: "Area") -> bool:
        """Test if this Area fits fully inside argument Area.

        Args:
            area: An Area to test this Area against.

        Returns:
            A bool which is True when this Area is inside argument Area.
        """
        return self.horizontal_inside(area) and self.vertical_inside(area)

    def inside_relative(self, area: "Area") -> bool:
        """Test if this Area fits fully inside argument Area when its
        coordinates are relative to the coordinates of the argument Area.

        Args:
            area: An Area to test this Area against.

        Returns:
            A bool which is True when this Area is inside argument Area.
        """
        return (
            (self.x >= 0)
            and (self.y >= 0)
            and (self.right() <= area.width)
            and (self.top() <= area.height)
        )

    def horizontal_inside(self, area: "Area") -> bool:
        """Test if this Area fits horizontally inside argument Area.

        Args:
            area: An Area to test this Area against.

        Returns:
            A bool which is True when this Area is inside argument Area.
        """
        return self.x >= area.x and self.right() <= area.right()

    def vertical_inside(self, area: "Area") -> bool:
        """Test if this Area fits vertically inside argument Area.

        Args:
            area: An Area to test this Area against.

        Returns:
            A bool which is True when this Area is inside argument Area.
        """
        return self.y >= area.y and self.top() <= area.top()

    def left_overlap(self, area: "Area") -> bool:
        """Test if this Area overlaps the left edge of argument Area.

        Does not include any test to see if they overlap vertically.

        Args:
            area: An Area to test this Area against.

        Returns:
            A bool which is True when this Area overlaps argument Area.
        """
        return self.x <= area.x and self.right() >= area.x

    def bottom_overlap(self, area: "Area") -> bool:
        """Test if this Area overlaps the bottom edge of argument Area.

        Does not include any test to see if they overlap horizontally.

        Args:
            area: An Area to test this Area against.

        Returns:
            A bool which is True when this Area overlaps argument Area.
        """
        return self.y <= area.y and self.top() >= area.y

    def right_overlap(self, area: "Area") -> bool:
        """Test if this Area overlaps the right edge of argument Area.

        Does not include any test to see if they overlap vertically.

        Args:
            area: An Area to test this Area against.

        Returns:
            A bool which is True when this Area overlaps argument Area.
        """
        return self.x <= area.right() and self.right() >= area.right()

    def top_overlap(self, area: "Area") -> bool:
        """Test if this Area overlaps the top edge of argument Area.

        Does not include any test to see if they overlap horizontally.

        Args:
            area: An Area to test this Area against.

        Returns:
            A bool which is True when this Area overlaps argument Area.
        """
        return self.y <= area.top() and self.top() >= area.top()

    def horizontal_overlap(self, area: "Area") -> bool:
        """Test if this Area horizontally overlaps any part of argument Area.

        Does not include any test to see if they overlap vertically.

        Args:
            area: An Area to test this Area against.

        Returns:
            A bool which is True when this Area overlaps argument Area.
        """
        inside = self.horizontal_inside(area)
        overlap_left = self.left_overlap(area)
        overlap_right = self.right_overlap(area)
        return inside or overlap_left or overlap_right

    def vertical_overlap(self, area: "Area") -> bool:
        """Test if this Area vertically overlaps any part of argument Area.

        Does not include any test to see if they overlap horizontally.

        Args:
            area: An Area to test this Area against.

        Returns:
            A bool which is True when this Area overlaps argument Area.
        """
        inside = self.vertical_inside(area)
        overlap_bottom = self.bottom_overlap(area)
        overlap_top = self.top_overlap(area)
        return inside or overlap_bottom or overlap_top

    def overlaps(self, area: "Area") -> bool:
        """Test if this overlaps any part of argument Area.

        Args:
            area: An Area to test this Area against.

        Returns:
            A bool which is True when this Area overlaps argument Area.
        """
        return self.horizontal_overlap(area) and self.vertical_overlap(area)

    def get_area_above(self, area: "Area", gap: float) -> "Area":
        """Create a new Area the same size as this Area above the argument
        Area.

        Args:
            area: An Area to create new Area above.
            gap: A float containing the distance new Area should be above
            argument Area.

        Returns:
            A new Area.
        """
        return Area(
            self.x, area.y + area.height + gap, self.width, self.height
        )

    def get_area_below(self, area: "Area", gap: float) -> "Area":
        """Create a new Area the same size as this Area below the argument
        Area.

        Args:
            area: An Area to create new Area above.
            gap: A float containing the distance new Area should be below
            argument Area.

        Returns:
            A new Area.
        """
        return Area(
            self.x, area.y - self.height - gap, self.width, self.height
        )

    def get_area_to_left(self, area: "Area", gap: float) -> "Area":
        """Create a new Area the same size as this Area to left of the
        argument Area.

        Args:
            area: An Area to create new Area above.
            gap: A float containing the distance new Area should be to left of
            argument Area.

        Returns:
            A new Area.
        """
        return Area(area.x - self.width - gap, self.y, self.width, self.height)

    def get_area_to_right(self, area: "Area", gap: float) -> "Area":
        """Create a new Area the same size as this Area to the right of the
        argument Area.

        Args:
            area: An Area to create new Area above.
            gap: A float containing the distance new Area should be to right
            of argument Area.

        Returns:
            A new Area.
        """
        return Area(area.x + area.width + gap, self.y, self.width, self.height)

    def __str__(self):
        """Describe this area as a String."""
        return f"Area(x={self.x} y={self.y} w={self.width} h={self.height})"
