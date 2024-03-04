from django.test import TestCase

from timelines.pdf.area import Area
from timelines.pdf.inside import Inside


class InsideTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.area_main = Area(5, 5, 10, 5)
        cls.area_relative_same = Area(0, 0, 10, 5)
        cls.area_relative_left_inside = Area(1, 0, 10, 5)
        cls.area_relative_left_not_inside = Area(-1, 0, 10, 5)
        cls.area_relative_bottom_inside = Area(0, 1, 10, 5)
        cls.area_relative_bottom_not_inside = Area(0, -1, 10, 5)
        cls.area_relative_right_inside = Area(-1, 0, 10, 5)
        cls.area_relative_right_not_inside = Area(1, 0, 10, 5)
        cls.area_relative_top_inside = Area(0, -1, 10, 5)
        cls.area_relative_top_not_inside = Area(0, 1, 10, 5)
        cls.area_left_inside = Area(6, 5, 10, 5)
        cls.area_left_not_inside = Area(4, 5, 10, 5)
        cls.area_bottom_inside = Area(5, 6, 10, 5)
        cls.area_bottom_not_inside = Area(5, 4, 10, 5)
        cls.area_right_inside = Area(4, 5, 10, 5)
        cls.area_right_not_inside = Area(6, 5, 10, 5)
        cls.area_top_inside = Area(5, 4, 10, 5)
        cls.area_top_not_inside = Area(5, 6, 10, 5)

    def test_relative_same(self):
        inside = Inside(self.area_relative_same, self.area_main, True)
        self.assertTrue(inside.left_inside)
        self.assertTrue(inside.bottom_inside)
        self.assertTrue(inside.right_inside)
        self.assertTrue(inside.top_inside)

    def test_relative_left_is_inside(self):
        inside = Inside(self.area_relative_left_inside, self.area_main, True)
        self.assertTrue(inside.left_inside)

    def test_relative_left_is_not_inside(self):
        inside = Inside(
            self.area_relative_left_not_inside, self.area_main, True
        )
        self.assertFalse(inside.left_inside)

    def test_relative_bottom_is_inside(self):
        inside = Inside(self.area_relative_right_inside, self.area_main, True)
        self.assertTrue(inside.bottom_inside)

    def test_relative_bottom_is_not_inside(self):
        inside = Inside(
            self.area_relative_bottom_not_inside, self.area_main, True
        )
        self.assertFalse(inside.bottom_inside)

    def test_relative_right_is_inside(self):
        inside = Inside(self.area_relative_right_inside, self.area_main, True)
        self.assertTrue(inside.right_inside)

    def test_relative_right_is_not_inside(self):
        inside = Inside(
            self.area_relative_right_not_inside, self.area_main, True
        )
        self.assertFalse(inside.right_inside)

    def test_relative_top_is_inside(self):
        inside = Inside(self.area_relative_top_inside, self.area_main, True)
        self.assertTrue(inside.top_inside)

    def test_relative_top_is_not_inside(self):
        inside = Inside(
            self.area_relative_top_not_inside, self.area_main, True
        )
        self.assertFalse(inside.top_inside)

    def test_same(self):
        inside = Inside(self.area_main, self.area_main, False)
        self.assertTrue(inside.left_inside)
        self.assertTrue(inside.bottom_inside)
        self.assertTrue(inside.right_inside)
        self.assertTrue(inside.top_inside)

    def test_left_is_inside(self):
        inside = Inside(self.area_left_inside, self.area_main, False)
        self.assertTrue(inside.left_inside)

    def test_left_is_not_inside(self):
        inside = Inside(self.area_left_not_inside, self.area_main, False)
        self.assertFalse(inside.left_inside)

    def test_bottom_is_inside(self):
        inside = Inside(self.area_bottom_inside, self.area_main, False)
        self.assertTrue(inside.bottom_inside)

    def test_bottom_is_not_inside(self):
        inside = Inside(self.area_bottom_not_inside, self.area_main, False)
        self.assertFalse(inside.bottom_inside)

    def test_right_is_inside(self):
        inside = Inside(self.area_right_inside, self.area_main, False)
        self.assertTrue(inside.right_inside)

    def test_right_is_not_inside(self):
        inside = Inside(self.area_right_not_inside, self.area_main, False)
        self.assertFalse(inside.right_inside)

    def test_top_is_inside(self):
        inside = Inside(self.area_top_inside, self.area_main, False)
        self.assertTrue(inside.top_inside)

    def test_top_is_not_inside(self):
        inside = Inside(self.area_top_not_inside, self.area_main, False)
        self.assertFalse(inside.top_inside)
