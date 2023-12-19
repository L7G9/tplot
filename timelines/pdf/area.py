class Area:
    """Class to represent an area as a rectangle."""

    def __init__(self, x: float, y: float, width: float, height: float):
        """Initialise Instance."""
        self.x: float = x
        self.y: float = y
        self.width: float = width
        self.height: float = height

    def copy_coordinates(self, area: "Area"):
        """Copy x and y coordinates from argument area to this area."""
        self.x = area.x
        self.y = area.y

    def copy_dimensions(self, area: "Area"):
        """Copy width and height from argument area to this area."""
        self.width = area.width
        self.height = area.height

    def copy(self, area: "Area"):
        """Copy coordinates and dimensions from argument area to this area."""
        self.copy_coordinates(area)
        self.copy_dimensions(area)

    def right(self) -> float:
        """Get x coordinate of the right most edge of this area."""
        return self.x + self.width

    def top(self) -> float:
        """Get y coordinate of the top most edge of this area."""
        return self.y + self.height

    def is_inside(self, area: "Area") -> bool:
        """Find if this area fits fully inside argument area."""
        return (
            (self.x >= area.x)
            and (self.y >= area.y)
            and (self.right() <= area.right())
            and (self.top() <= area.top())
        )

    def is_inside_relative(self, area: "Area") -> bool:
        """Find if this area fits fully inside argument area when its
        coordinates are relative to the coordinates of the argument area."""
        return (
            (self.x >= 0)
            and (self.y >= 0)
            and (self.right() <= area.width)
            and (self.top() <= area.height)
        )

    def overlaps(self, area: "Area") -> bool:
        """Find in this area overlaps argument area."""
        inside = self.is_inside(area)
        overlap_left = self.x <= area.x and self.right() >= area.x
        overlap_bottom = self.y <= area.y and self.top() >= area.y
        overlap_right = self.x <= area.right() and self.right() >= area.right()
        overlap_top = self.y <= area.top() and self.top() >= area.top()
        return inside or (
            (overlap_left or overlap_right) and (overlap_bottom or overlap_top)
        )

    def get_area_above(self, area: "Area", gap: float) -> "Area":
        """Create a new area the same size as this one above the argument area."""
        return Area(
            self.x, area.y + area.height + gap, self.width, self.height
        )

    def get_area_below(self, area: "Area", gap: float) -> "Area":
        """Create a new area the same size as this one below the argument area."""
        return Area(
            self.x, area.y - self.height - gap, self.width, self.height
        )

    def get_area_to_left(self, area: "Area", gap: float) -> "Area":
        """Create a new area the same size as this one to the left of the argument area."""
        return Area(area.x - self.width - gap, self.y, self.width, self.height)

    def get_area_to_right(self, area: "Area", gap: float) -> "Area":
        """Create a new area the same size as this one to the left of the argument area."""
        return Area(area.x + area.width + gap, self.y, self.width, self.height)

    def __str__(self):
        return f"Area(x={self.x} y={self.y} w={self.width} h={self.height})"
