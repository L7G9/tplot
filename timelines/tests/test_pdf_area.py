from django.contrib.auth.models import User
from django.test import TestCase

from timelines.pdf.area import Area

class AreaTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.area = Area(2, 2, 4, 4)
        self.area_same = Area(2, 2, 4, 4)
        self.area_surround = Area(1, 1, 6, 6)
        self.area_far = Area(10, 10, 4, 4)
        self.area_inside = Area(3, 3, 2, 2)
        self.area_left = Area(1,3,4,2)
        self.area_right = Area(3,3,4,2)
        self.area_bottom = Area(3,1,2,4)
        self.area_top = Area(3,3,2,4)

    def test_right(self):
        right = self.area.right()
        self.assertEqual(right, 6)

    def test_top(self):
        top = self.area.top()
        self.assertEqual(top, 6)

    def test_inside_same_area(self):
        inside = self.area.is_inside(self.area_same)
        self.assertEqual(inside, True)

    def test_inside_surrounding_area(self):
        inside = self.area.is_inside(self.area_surround)
        self.assertEqual(inside, True)

    def test_inside_far_area(self):
        inside = self.area.is_inside(self.area_far)
        self.assertEqual(inside, False)

    def test_inside_inside_area(self):
        inside = self.area.is_inside(self.area_inside)
        self.assertEqual(inside, False)

    def test_inside_left_overlap_area(self):
        inside = self.area.is_inside(self.area_left)
        self.assertEqual(inside, False)

    def test_inside_right_overlap(self):
        inside = self.area.is_inside(self.area_right)
        self.assertEqual(inside, False)

    def test_inside_bottom_overlap(self):
        inside = self.area.is_inside(self.area_bottom)
        self.assertEqual(inside, False)

    def test_inside_top_overlap(self):
        inside = self.area.is_inside(self.area_top)
        self.assertEqual(inside, False)

    def test_overlap_same_area(self):
        inside = self.area.overlaps(self.area_same)
        self.assertEqual(inside, True)

    def test_overlap_surrounding_area(self):
        inside = self.area.overlaps(self.area_surround)
        self.assertEqual(inside, True)

    def test_overlap_far_area(self):
        inside = self.area.overlaps(self.area_far)
        self.assertEqual(inside, False)

    def test_overlap_inside_area(self):
        inside = self.area.overlaps(self.area_inside)
        self.assertEqual(inside, True)

    def test_overlap_left_overlap_area(self):
        inside = self.area.overlaps(self.area_left)
        self.assertEqual(inside, True)

    def test_overlap_right_overlap(self):
        inside = self.area.overlaps(self.area_right)
        self.assertEqual(inside, True)

    def test_overlap_bottom_overlap(self):
        inside = self.area.overlaps(self.area_bottom)
        self.assertEqual(inside, True)

    def test_overlap_top_overlap(self):
        inside = self.area.overlaps(self.area_top)
        self.assertEqual(inside, True)
