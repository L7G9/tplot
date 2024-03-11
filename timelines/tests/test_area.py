from django.test import TestCase

from timelines.pdf.area import Area

MAIN_X = 5.0
MAIN_Y = 6.0
MAIN_W = 10.0
MAIN_H = 11.0
COPY_COORD = 1.0
COPY_SIZE = 2.0
GAP = 1.0


class AreaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.main_area = Area(MAIN_X, MAIN_Y, MAIN_W, MAIN_H)

    def test_copy_coordinates(self):
        test_area = Area(COPY_COORD, COPY_COORD, COPY_SIZE, COPY_SIZE)
        test_area.copy_coordinates(self.main_area)
        self.assertEqual(test_area.x, MAIN_X)
        self.assertEqual(test_area.y, MAIN_Y)
        self.assertEqual(test_area.width, COPY_SIZE)
        self.assertEqual(test_area.height, COPY_SIZE)

    def test_copy_dimensions(self):
        test_area = Area(COPY_COORD, COPY_COORD, COPY_SIZE, COPY_SIZE)
        test_area.copy_dimensions(self.main_area)
        self.assertEqual(test_area.x, COPY_COORD)
        self.assertEqual(test_area.y, COPY_COORD)
        self.assertEqual(test_area.width, MAIN_W)
        self.assertEqual(test_area.height, MAIN_H)

    def test_copy(self):
        test_area = Area(COPY_COORD, COPY_COORD, COPY_SIZE, COPY_SIZE)
        test_area.copy(self.main_area)
        self.assertEqual(test_area.x, MAIN_X)
        self.assertEqual(test_area.y, MAIN_Y)
        self.assertEqual(test_area.width, MAIN_W)
        self.assertEqual(test_area.height, MAIN_H)

    def test_right(self):
        self.assertEqual(self.main_area.right(), MAIN_X + MAIN_W)

    def test_top(self):
        self.assertEqual(self.main_area.top(), MAIN_Y + MAIN_H)

    def test_horizontal_inside_all_left(self):
        test_area = Area(MAIN_X - 3.0, MAIN_Y, 2.0, MAIN_H)
        self.assertFalse(test_area.horizontal_inside(self.main_area))

    def test_horizontal_inside_overlap_left(self):
        test_area = Area(MAIN_X - 1.0, MAIN_Y, 2.0, MAIN_H)
        self.assertFalse(test_area.horizontal_inside(self.main_area))

    def test_horizontal_inside_all_right(self):
        test_area = Area(MAIN_X + MAIN_W + 1.0, MAIN_Y, 2.0, MAIN_H)
        self.assertFalse(test_area.horizontal_inside(self.main_area))

    def test_horizontal_inside_overlap_right(self):
        test_area = Area(MAIN_X + MAIN_W - 1.0, MAIN_Y, 2.0, MAIN_H)
        self.assertFalse(test_area.horizontal_inside(self.main_area))

    def test_horizontal_inside_smaller(self):
        test_area = Area(MAIN_X + 1.0, MAIN_Y, MAIN_W - 2.0, MAIN_H)
        self.assertTrue(test_area.horizontal_inside(self.main_area))

    def test_horizontal_inside_same(self):
        test_area = Area(MAIN_X, MAIN_Y, MAIN_W, MAIN_H)
        self.assertTrue(test_area.horizontal_inside(self.main_area))

    def test_vertical_inside_all_below(self):
        test_area = Area(MAIN_X, MAIN_Y - 3.0, MAIN_W, 2.0)
        self.assertFalse(test_area.vertical_inside(self.main_area))

    def test_vertical_inside_overlap_bottom(self):
        test_area = Area(MAIN_X, MAIN_Y - 1.0, MAIN_W, 2.0)
        self.assertFalse(test_area.vertical_inside(self.main_area))

    def test_vertical_inside_all_above(self):
        test_area = Area(MAIN_X, MAIN_Y + MAIN_H + 1.0, MAIN_W, 2.0)
        self.assertFalse(test_area.vertical_inside(self.main_area))

    def test_vertical_inside_overlap_top(self):
        test_area = Area(MAIN_X, MAIN_Y + MAIN_H - 1.0, MAIN_W, 2.0)
        self.assertFalse(test_area.vertical_inside(self.main_area))

    def test_vertical_inside_smaller(self):
        test_area = Area(MAIN_X, MAIN_Y + 1.0, MAIN_W, MAIN_H - 2.0)
        self.assertTrue(test_area.vertical_inside(self.main_area))

    def test_vertical_inside_same(self):
        test_area = Area(MAIN_X, MAIN_Y, MAIN_W, MAIN_H)
        self.assertTrue(test_area.vertical_inside(self.main_area))

    def test_inside_none(self):
        test_area = Area(0, 0, MAIN_W, MAIN_H)
        self.assertFalse(test_area.inside(self.main_area))

    def test_inside_horizontal_only(self):
        test_area = Area(MAIN_X, 0, MAIN_W, MAIN_H)
        self.assertFalse(test_area.inside(self.main_area))

    def test_inside_vertical_only(self):
        test_area = Area(0, MAIN_Y, MAIN_W, MAIN_H)
        self.assertFalse(test_area.inside(self.main_area))

    def test_inside_smaller(self):
        test_area = Area(
            MAIN_X + 1.0, MAIN_Y + 1.0, MAIN_W - 2.0, MAIN_H - 2.0
        )
        self.assertTrue(test_area.inside(self.main_area))

    def test_inside_same(self):
        test_area = Area(MAIN_X, MAIN_Y, MAIN_W, MAIN_H)
        self.assertTrue(test_area.inside(self.main_area))

    def test_inside_relative_none(self):
        test_area = Area(MAIN_W + 1.0, 0, MAIN_W, MAIN_H)
        self.assertFalse(test_area.inside_relative(self.main_area))

    def test_inside_relative_horizontal_only(self):
        test_area = Area(0, 1.0, MAIN_W, MAIN_H)
        self.assertFalse(test_area.inside_relative(self.main_area))

    def test_inside_relative_vertical_only(self):
        test_area = Area(1.0, 0, MAIN_W, MAIN_H)
        self.assertFalse(test_area.inside_relative(self.main_area))

    def test_inside_relative_smaller(self):
        test_area = Area(1.0, 1.0, MAIN_W - 2.0, MAIN_H - 2.0)
        self.assertTrue(test_area.inside_relative(self.main_area))

    def test_left_overlap_all_left(self):
        test_area = Area(MAIN_X - 3.0, MAIN_Y, 2.0, MAIN_H)
        self.assertFalse(test_area.left_overlap(self.main_area))

    def test_left_overlap_all_right(self):
        test_area = Area(MAIN_X + 1.0, MAIN_Y, 2.0, MAIN_H)
        self.assertFalse(test_area.left_overlap(self.main_area))

    def test_left_overlap_overlaps(self):
        test_area = Area(MAIN_X - 1.0, MAIN_Y, 2.0, MAIN_H)
        self.assertTrue(test_area.left_overlap(self.main_area))

    def test_bottom_overlap_all_under(self):
        test_area = Area(MAIN_X, MAIN_Y - 3.0, MAIN_W, 2.0)
        self.assertFalse(test_area.bottom_overlap(self.main_area))

    def test_bottom_overlap_all_above(self):
        test_area = Area(MAIN_X, MAIN_Y + 1.0, MAIN_W, 2.0)
        self.assertFalse(test_area.bottom_overlap(self.main_area))

    def test_bottom_overlap_overlaps(self):
        test_area = Area(MAIN_X, MAIN_Y - 1.0, MAIN_W, 2.0)
        self.assertTrue(test_area.bottom_overlap(self.main_area))

    def test_right_overlap_all_left(self):
        test_area = Area(MAIN_X + MAIN_W - 3.0, MAIN_Y, 2.0, MAIN_H)
        self.assertFalse(test_area.right_overlap(self.main_area))

    def test_right_overlap_all_right(self):
        test_area = Area(MAIN_X + MAIN_W + 1.0, MAIN_Y, 2.0, MAIN_H)
        self.assertFalse(test_area.right_overlap(self.main_area))

    def test_right_overlap_overlaps(self):
        test_area = Area(MAIN_X + MAIN_W - 1.0, MAIN_Y, 2.0, MAIN_H)
        self.assertTrue(test_area.right_overlap(self.main_area))

    def test_top_overlap_all_under(self):
        test_area = Area(MAIN_X, MAIN_Y + MAIN_H - 3.0, MAIN_W, 2.0)
        self.assertFalse(test_area.top_overlap(self.main_area))

    def test_top_overlap_all_above(self):
        test_area = Area(MAIN_X, MAIN_Y + MAIN_H + 1.0, MAIN_W, 2.0)
        self.assertFalse(test_area.top_overlap(self.main_area))

    def test_top_overlap_overlaps(self):
        test_area = Area(MAIN_X, MAIN_Y + MAIN_H - 1.0, MAIN_W, 2.0)
        self.assertTrue(test_area.top_overlap(self.main_area))

    def test_horizontal_overlap_fully_left(self):
        test_area = Area(MAIN_X - 3.0, MAIN_Y, 2.0, MAIN_H)
        self.assertFalse(test_area.horizontal_overlap(self.main_area))

    def test_horizontal_overlap_partially_left(self):
        test_area = Area(MAIN_X - 1.0, MAIN_Y, 2.0, MAIN_H)
        self.assertTrue(test_area.horizontal_overlap(self.main_area))

    def test_horizontal_overlap_fully_inside(self):
        test_area = Area(MAIN_X + 1.0, MAIN_Y, 2.0, MAIN_H)
        self.assertTrue(test_area.horizontal_overlap(self.main_area))

    def test_horizontal_overlap_fully_surrounding(self):
        test_area = Area(MAIN_X - 1.0, MAIN_Y, MAIN_W + 2.0, MAIN_H)
        self.assertTrue(test_area.horizontal_overlap(self.main_area))

    def test_horizontal_overlap_partially_right(self):
        test_area = Area(MAIN_X + MAIN_W - 1.0, MAIN_Y, 2.0, MAIN_H)
        self.assertTrue(test_area.horizontal_overlap(self.main_area))

    def test_horizontal_overlap_fully_right(self):
        test_area = Area(MAIN_X + MAIN_W + 1.0, MAIN_Y, 2.0, MAIN_H)
        self.assertFalse(test_area.horizontal_overlap(self.main_area))

    def test_vertical_overlap_fully_under(self):
        test_area = Area(MAIN_X, MAIN_Y - 3.0, MAIN_W, 2.0)
        self.assertFalse(test_area.vertical_overlap(self.main_area))

    def test_vertical_overlap_partially_under(self):
        test_area = Area(MAIN_X, MAIN_Y - 1.0, MAIN_W, 2.0)
        self.assertTrue(test_area.vertical_overlap(self.main_area))

    def test_vertical_overlap_fully_inside(self):
        test_area = Area(MAIN_X, MAIN_Y + 1.0, MAIN_W, 2.0)
        self.assertTrue(test_area.vertical_overlap(self.main_area))

    def test_vertical_overlap_fully_surrounding(self):
        test_area = Area(MAIN_X, MAIN_Y - 1.0, MAIN_W, MAIN_H + 2.0)
        self.assertTrue(test_area.vertical_overlap(self.main_area))

    def test_vertical_overlap_partially_above(self):
        test_area = Area(MAIN_X, MAIN_Y + MAIN_H - 1.0, MAIN_W, 2.0)
        self.assertTrue(test_area.vertical_overlap(self.main_area))

    def test_vertical_overlap_fully_above(self):
        test_area = Area(MAIN_X, MAIN_Y + MAIN_H + 1.0, MAIN_W, 2.0)
        self.assertFalse(test_area.vertical_overlap(self.main_area))

    def test_overlaps_outside_left(self):
        test_area = Area(MAIN_X - 3.0, MAIN_Y, 2.0, MAIN_H)
        self.assertFalse(test_area.overlaps(self.main_area))

    def test_overlaps_outside_under(self):
        test_area = Area(MAIN_X, MAIN_Y - 3.0, MAIN_W, 2.0)
        self.assertFalse(test_area.overlaps(self.main_area))

    def test_overlaps_outside_right(self):
        test_area = Area(MAIN_X + MAIN_W + 1.0, MAIN_Y, 2.0, MAIN_H)
        self.assertFalse(test_area.overlaps(self.main_area))

    def test_overlaps_outside_above(self):
        test_area = Area(MAIN_X, MAIN_Y + MAIN_H + 1.0, MAIN_W, 2.0)
        self.assertFalse(test_area.overlaps(self.main_area))

    def test_overlaps_left(self):
        test_area = Area(MAIN_X - 1.0, MAIN_Y, 2.0, MAIN_H)
        self.assertTrue(test_area.overlaps(self.main_area))

    def test_overlaps_bottom(self):
        test_area = Area(MAIN_X, MAIN_Y - 1.0, MAIN_W, 2.0)
        self.assertTrue(test_area.overlaps(self.main_area))

    def test_overlaps_right(self):
        test_area = Area(MAIN_X + MAIN_W - 1.0, MAIN_Y, 2.0, MAIN_H)
        self.assertTrue(test_area.overlaps(self.main_area))

    def test_overlaps_top(self):
        test_area = Area(MAIN_X, MAIN_Y + MAIN_H - 1.0, MAIN_W, 2.0)
        self.assertTrue(test_area.overlaps(self.main_area))

    def test_overlaps_inside(self):
        test_area = Area(
            MAIN_X + 1.0, MAIN_Y + 1.0, MAIN_W - 2.0, MAIN_H - 2.0
        )
        self.assertTrue(test_area.overlaps(self.main_area))

    def test_overlaps_surrounding(self):
        test_area = Area(
            MAIN_X - 1.0, MAIN_Y - 1.0, MAIN_W + 2.0, MAIN_H + 2.0
        )
        self.assertTrue(test_area.overlaps(self.main_area))

    def test_get_area_above(self):
        test_area = Area(COPY_COORD, COPY_COORD, COPY_SIZE, COPY_SIZE)
        result_area = test_area.get_area_above(self.main_area, GAP)
        self.assertEqual(result_area.x, COPY_COORD)
        self.assertEqual(result_area.y, MAIN_Y + MAIN_H + GAP)
        self.assertEqual(result_area.width, COPY_SIZE)
        self.assertEqual(result_area.height, COPY_SIZE)

    def test_get_area_below(self):
        test_area = Area(COPY_COORD, COPY_COORD, COPY_SIZE, COPY_SIZE)
        result_area = test_area.get_area_below(self.main_area, GAP)
        self.assertEqual(result_area.x, COPY_COORD)
        self.assertEqual(result_area.y, MAIN_Y - COPY_SIZE - GAP)
        self.assertEqual(result_area.width, COPY_SIZE)
        self.assertEqual(result_area.height, COPY_SIZE)

    def test_get_area_to_left(self):
        test_area = Area(COPY_COORD, COPY_COORD, COPY_SIZE, COPY_SIZE)
        result_area = test_area.get_area_to_left(self.main_area, GAP)
        self.assertEqual(result_area.x, MAIN_X - COPY_SIZE - GAP)
        self.assertEqual(result_area.y, COPY_COORD)
        self.assertEqual(result_area.width, COPY_SIZE)
        self.assertEqual(result_area.height, COPY_SIZE)

    def test_get_area_to_right(self):
        test_area = Area(COPY_COORD, COPY_COORD, COPY_SIZE, COPY_SIZE)
        result_area = test_area.get_area_to_right(self.main_area, GAP)
        self.assertEqual(result_area.x, MAIN_X + MAIN_W + GAP)
        self.assertEqual(result_area.y, COPY_COORD)
        self.assertEqual(result_area.width, COPY_SIZE)
        self.assertEqual(result_area.height, COPY_SIZE)
