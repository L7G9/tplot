from .area import Area


class Inside:
    def __init__(self, area1: Area, area2: Area, relative: bool = True):
        if relative:
            self.left_inside = area1.x >= 0
            self.bottom_inside = area1.y >= 0
            self.right_inside = area1.right() <= area2.width
            self.top_inside = area1.top() <= area2.height
        else:
            self.left_inside = area1.x >= area2.x
            self.bottom_inside = area1.y >= area2.y
            self.right_inside = area1.right() <= area2.right()
            self.top_inside = area1.top() <= area2.top()

    def test(
        self,
        left_inside: bool = True,
        bottom_inside: bool = True,
        right_inside: bool = True,
        top_inside: bool = True
    ) -> bool:
        return (
            left_inside is self.left_inside
            and bottom_inside is self.bottom_inside
            and right_inside is self.right_inside
            and top_inside is self.top_inside
        )
