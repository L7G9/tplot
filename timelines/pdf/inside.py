"""Contains class to test which parts of ann Area instance are inside another.

Classes:
    Inside

Usage:
    inner_area = Area(5, 5, 10, 5)
    outer_area = Area(0, 0, 20, 15)
    inside = Inside(inner_area, outer_area, True)

    is_fully_inside = inside.test()
    inside_with_right_hand_side_overlap = inside.text(right_inside=False)
"""
from .area import Area


class Inside:
    """Class to test which sides of an Area are inside another.

    Attributes:
        left_inside: A bool set to True if area1's left edge is to the right
        of area2's left edge.
        bottom_inside: A bool set to True if area1's bottom edge is above
        area2's bottom edge.
        right_inside: A bool set to True if area1's right edge is to the left
        of area2's right edge.
        top_inside: A bool set to True if area1's top edge is under area2's
        top edge.
    """

    # TODO: look for replication of functionality with methods in Area
    def __init__(self, area1: Area, area2: Area, relative: bool = True):
        """Initialise Instance.

        Args:
            area1: An Area instance to test if it fits inside area2.
            area2: An Area instance to test if area1 fits inside it.
            relative: A bool set to True when area1's coordinates are
            relative to the position of  area2.  Default is True.
        """
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
        top_inside: bool = True,
    ) -> bool:
        """Initialise Instance.

        Args:
            left_inside: A bool to test value of left_inside attribute.
            Default is True.
            bottom_inside: A bool to test value of bottom_inside attribute.
            Default is True.
            right_inside: A bool to test value of right_inside attribute.
            Default is True.
            top_inside: A bool to test value of top_inside attribute.  Default
            is True.

        Returns:
            A bool return True when all arguments are equal to their
            corresponding attribute.
        """
        return (
            left_inside is self.left_inside
            and bottom_inside is self.bottom_inside
            and right_inside is self.right_inside
            and top_inside is self.top_inside
        )

    def __str__(self):
        """Describe instance as a string"""
        return f"Inside(left={self.left_inside} bottom={self.bottom_inside} \
        right={self.right_inside} top={self.top_inside})"
