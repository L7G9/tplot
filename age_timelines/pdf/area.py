class Area:
    def __init__(self, x: int, y: int, width: int, height: int, object=None):
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.object = object
        self.children = []

    def right(self) -> int:
        return self.x + self.width

    def top(self) -> int:
        return self.y + self.height

    def is_inside(self, area: "Area") -> bool:
        return (
            (self.x >= area.x)
            and (self.y >= area.y)
            and (self.right() <= area.right())
            and (self.top() <= area.top())
        )

    def overlaps(self, area: "Area") -> bool:
        inside = self.is_inside(area)
        overlap_left = self.x <= area.x and self.right() >= area.x
        overlap_bottom = self.y <= area.y and self.top() >= area.y
        overlap_right = self.x <= area.right() and self.right() >= area.right()
        overlap_top = self.y <= area.top() and self.top() >= area.top()
        return (
            inside
            or overlap_left
            or overlap_bottom
            or overlap_right
            or overlap_top
        )
